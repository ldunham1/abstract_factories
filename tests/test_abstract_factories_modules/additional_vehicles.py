from .abstract import VehicleAbstract
from . import additional_additional_vehicles


class JetSki(VehicleAbstract):

    def start(self):
        print("Starting {} {} {} jetski.".format(self.year, self.make, self.model))

    def stop(self):
        print("Stopping {} {} {} jetski.".format(self.year, self.make, self.model))


# ------------------------------------------------------------------------------
# Instances
jetski1 = JetSki('Kawasaki', 'Ultra LX', 2021)
jetski2 = JetSki('Yamaha', 'FX SVH0', 2024)
