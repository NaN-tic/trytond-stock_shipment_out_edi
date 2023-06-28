from trytond.pool import PoolMeta


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    def create_shipment(self, shipment_type):
        shipments = super().create_shipment(shipment_type)

        if shipment_type != 'out' or not shipments:
            return shipments

        for shipment in shipments:
            shipment.edi = True
            if self.reference and self.number:
                shipment.reference = self.reference + '-' + self.number
        return shipments
