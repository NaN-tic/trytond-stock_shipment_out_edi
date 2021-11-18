# -*- coding: utf-8 -*
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class StockConfiguration(metaclass=PoolMeta):
    __name__ = 'stock.configuration'

    outbox_path_edi = fields.Char('EDI Shipment Outbox Path')
    automatic_edi_shipment_out = fields.Boolean('Send EDI file automatically')

    @classmethod
    def default_automatic_edi_shipment_out(cls):
        return True
