class VehicleAbstract:
    """
    An abstract base class for vehicles.
    """
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    @property
    def name(self):
        return '{} {}'.format(self.make, self.model)

    def start(self):
        raise NotImplementedError("Subclasses must implement the 'start' method.")

    def stop(self):
        raise NotImplementedError("Subclasses must implement the 'stop' method.")
