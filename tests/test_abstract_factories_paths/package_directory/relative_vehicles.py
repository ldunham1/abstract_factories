from .vehicles import Truck


class PedaloTruck(Truck):

    def start(self):
        print("Starting {} {} pedalo.".format(self.year, self.make))

    def stop(self):
        print("Stopping {} {} pedalo.".format(self.year, self.make))


# ------------------------------------------------------------------------------
# Instances
pedalo_truck1 = PedaloTruck('SunFun', 'Sand', 1989)
