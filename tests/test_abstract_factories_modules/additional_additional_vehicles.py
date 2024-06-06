from .abstract import VehicleAbstract


class Horse(VehicleAbstract):

    def start(self):
        print("Starting {} {} {} horse.".format(self.year, self.make, self.model))

    def stop(self):
        print("Stopping {} {} {} horse.".format(self.year, self.make, self.model))


# ------------------------------------------------------------------------------
# Instances
horse1 = Horse('Arabian', 'Bay', 2021)
horse2 = Horse('Coconuts', 'Brown', 1975)
