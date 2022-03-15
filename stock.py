# -*- coding: utf-8 -*
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import os
from jinja2 import Template
from trytond.model import Workflow, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Not
from trytond.transaction import Transaction
from trytond.exceptions import UserWarning
from trytond.i18n import gettext

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

    is_edi = fields.Boolean('Is EDI')

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        cls._buttons.update({
                'generate_edi_file': {'invisible': (
                        Not(Eval('is_edi')) |
                        (Eval('state') != 'done')
                        )},
                })

    @classmethod
    @ModelView.button
    def generate_edi_file(cls, shipments):
        pool = Pool()
        Configuration = pool.get('stock.configuration')
        Warning = pool.get('res.user.warning')

        done_edi_shipment = Transaction().context.get(
            'done_edi_shipment', False)
        if done_edi_shipment:
            configuration = Configuration(1)
            if not configuration.automatic_edi_shipment_out:
                return

        for shipment in shipments:
            if shipment.is_edi:
                if done_edi_shipment:
                    warning_name = '%s.send_edi_shipment' % shipment
                    if Warning.check(warning_name):
                        raise UserWarning(warning_name, gettext(
                                'stock_shipment_out_edi.msg_send_edi_shipment',
                                shipment=shipment.number))
                shipment.generate_edi()

    @classmethod
    @ModelView.button
    @Workflow.transition('done')
    def done(cls, shipments):
        super(ShipmentOut, cls).done(shipments)
        with Transaction().set_context(done_edi_shipment=True):
            cls.generate_edi_file(shipments)

    def generate_edi(self):
        pool = Pool()
        StockConfiguration = pool.get('stock.configuration')
        config = StockConfiguration(1)
        template_name = 'shipment_out_edi_template.jinja2'
        result_name = 'shipment_{}.PLA'.format(self.number)
        template_path = os.path.join(MODULE_PATH, template_name)
        result_path = os.path.join(config.outbox_path_edi, result_name)
        if self.is_edi:
            with open(template_path) as file_:
                template = Template(file_.read())
            edi_file = template.render({'shipment': self, 'UOMS': UOMS})
            with open(result_path, 'w') as f:
                f.write(edi_file)

    @property
    def edi_operational_point_head(self):
        SaleLine = Pool().get('sale.line')

        for m in self.outgoing_moves:
            if m.origin and isinstance(m.origin, SaleLine):
                return m.origin.sale.party.edi_operational_point_head


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'

    code_ean13 = fields.Function(fields.Char("Code EAN13"), 'get_code_ean13')

    def get_code_ean13(self, name):
        if self.product:
            for identifier in self.product.identifiers:
                if identifier.type == 'ean' and len(identifier.code) == 13:
                    return identifier.code
        return None
