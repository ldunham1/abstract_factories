from .abstract import VehicleAbstract


class Car(VehicleAbstract):

    def start(self):
        print("Starting {} {} {} car.".format(self.year, self.make, self.model))

    def stop(self):
        print("Stopping {} {} {} car.".format(self.year, self.make, self.model))


class Truck(VehicleAbstract):

    def start(self):
        print("Starting {} {} {} truck.".format(self.year, self.make, self.model))

    def stop(self):
        print("Stopping {} {} {} truck.".format(self.year, self.make, self.model))


class Truck2(Truck):

    def stop(self):
        print('About to stop...')
        super(Truck2, self).stop()


class Motorcycle(VehicleAbstract):

    def start(self):
        print("Starting {} {} {} motorcycle.".format(self.year, self.make, self.model))

    def stop(self):
        print("Stopping {} {} {} motorcycle.".format(self.year, self.make, self.model))


# ------------------------------------------------------------------------------
# Instances
car1 = Car('Toyota', 'Camry', 2020)
car2 = Car('Ford', 'Fiesta', 1987)

truck1 = Truck('Ford', 'F-150', 2018)
truck2 = Truck2('Ford', 'F-150', 2020)

motorcycle1 = Motorcycle('Honda', 'CBR', 2004)
motorcycle2 = Motorcycle('Honda', 'CBR', 2008)
motorcycle3 = Motorcycle('Yamaha', 'R3', 2012)
