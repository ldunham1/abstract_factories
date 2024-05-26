class VehicleAbstract:
    """
    An abstract base class for vehicles.
    """
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def start(self):
        raise NotImplementedError("Subclasses must implement the 'start' method.")

    def stop(self):
        raise NotImplementedError("Subclasses must implement the 'stop' method.")
