# -*- coding: utf-8 -*
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Bool, Eval


class StockConfiguration(metaclass=PoolMeta):
    __name__ = 'stock.configuration'

    outbox_path_edi = fields.Char('EDI Shipment Outbox Path',
        states={
            'required': Bool(Eval('automatic_edi_shipment_out')),
        })
    automatic_edi_shipment_out = fields.Boolean('Send EDI file automatically')
