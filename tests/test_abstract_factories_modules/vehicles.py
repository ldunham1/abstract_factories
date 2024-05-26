from .abstract import VehicleAbstract


class Car(VehicleAbstract):

    def start(self):
        print(f"Starting {self.year} {self.make} {self.model} car.")

    def stop(self):
        print(f"Stopping {self.year} {self.make} {self.model} car.")


class Truck(VehicleAbstract):

    def start(self):
        print(f"Starting {self.year} {self.make} {self.model} truck.")

    def stop(self):
        print(f"Stopping {self.year} {self.make} {self.model} truck.")


class Truck2(Truck):

    def stop(self):
        print('About to stop...')
        super(Truck2, self).stop()


class Motorcycle(VehicleAbstract):

    def start(self):
        print(f"Starting {self.year} {self.make} {self.model} motorcycle.")

    def stop(self):
        print(f"Stopping {self.year} {self.make} {self.model} motorcycle.")


# ------------------------------------------------------------------------------
# Instances
car1 = Car('Toyota', 'Camry', 2020)
car2 = Car('Ford', 'Fiesta', 1987)

truck1 = Truck('Ford', 'F-150', 2018)
truck2 = Truck2('Ford', 'F-150', 2020)

motorcycle1 = Motorcycle('Honda', 'CBR', 2004)
motorcycle2 = Motorcycle('Honda', 'CBR', 2008)
motorcycle3 = Motorcycle('Yamaha', 'R3', 2012)
