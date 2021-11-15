# This file is part stock_shipment_out_edi module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import stock
from . import sale


def register():
    Pool.register(
        stock.ShipmentOut,
        stock.StockConfiguration,
        stock.Move,
        sale.Sale,
        module='stock_shipment_out_edi', type_='model')
    Pool.register(
        module='stock_shipment_out_edi', type_='wizard')
    Pool.register(
        module='stock_shipment_out_edi', type_='report')
