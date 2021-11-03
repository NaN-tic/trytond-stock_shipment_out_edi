from trytond.pool import PoolMeta


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    def create_shipment(self, shipment_type):
        shipment = super().create_shipment(shipment_type)
        if shipment and shipment_type == 'out' and self.edi:
            shipment[0].edi = True
            if self.reference and self.number:
                shipment[0].reference = self.reference + '-' + self.number
            shipment[0].save()
        return shipment
