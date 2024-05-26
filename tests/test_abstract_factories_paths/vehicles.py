from test_abstract_factories_paths.abstract import VehicleAbstract


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
