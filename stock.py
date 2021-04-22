import os
from jinja2 import Template
from trytond.model import Workflow, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

UOMS = {
        'kg': 'KGM',
        'u': 'PCE',
        'l': 'LTR',
        'g': 'GRM',
        'm': 'MTR',
        }


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    from_edi = fields.Function(fields.Boolean('From EDI?'), 'get_from_edi')

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        cls._buttons.update({
                'generate_edi_file': {'invisible': Eval('state') != 'done', },
                })

    def get_from_edi(self, name):
        # TODO: RETURN IF THE SALE FROM ORIGIN IS CREATED FORM EDI
        return True

    @classmethod
    @ModelView.button
    def generate_edi_file(cls, shipments):
        for shipment in shipments:
            shipment.generate_edi()

    @classmethod
    @ModelView.button
    @Workflow.transition('done')
    def done(cls, shipments):
        super(ShipmentOut, cls).done(shipments)
        cls.generate_edi_file(shipments)

    def generate_edi(self):
        pool = Pool()
        StockConfiguration = pool.get('stock.configuration')
        config = StockConfiguration(1)
        template_name = 'shipment_out_edi_template.jinja2'
        result_name = 'shipment_{}.PLA'.format(self.number)
        template_path = os.path.join(MODULE_PATH, template_name)
        result_path = os.path.join(config.outbox_path_edi, result_name)

        if self.from_edi:
            with open(template_path) as file_:
                template = Template(file_.read())
            edi_file = template.render({'shipment': self, 'UOMS': UOMS})
            with open(result_path, 'w') as f:
                f.write(edi_file)


class StockConfiguration(metaclass=PoolMeta):
    __name__ = 'stock.configuration'

    outbox_path_edi = fields.Char('Outbox Path EDI')
