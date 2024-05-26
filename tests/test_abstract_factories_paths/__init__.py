import os.path
from unittest.mock import patch
import unittest

from .abstract import VehicleAbstract
from abstract_factories import SimpleFactory

try:
    from io import StringIO
except ImportError:
    from unittest.mock import StringIO


class TestVehicleFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.VehicleFactory = SimpleFactory(VehicleAbstract, paths=[os.path.dirname(__file__)], name_key='__name__')

    def test_get_car(self):
        car = self.VehicleFactory.get('Car')
        car_instance = car('Toyota', 'Camry', 2020)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            car_instance.start()
            car_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2020 Toyota Camry car.\n"
                                              "Stopping 2020 Toyota Camry car.\n")

    def test_get_truck(self):
        truck = self.VehicleFactory.get('Truck')
        truck_instance = truck('Ford', 'F-150', 2018)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            truck_instance.start()
            truck_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2018 Ford F-150 truck.\n"
                                              "Stopping 2018 Ford F-150 truck.\n")

    def test_get_truck2(self):
        truck = self.VehicleFactory.get('Truck2')
        truck_instance = truck('Ford', 'F-150', 2018)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            truck_instance.start()
            truck_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2018 Ford F-150 truck.\n"
                                              "About to stop...\n"
                                              "Stopping 2018 Ford F-150 truck.\n")

    def test_get_motorcycle(self):
        motorcycle = self.VehicleFactory.get('Motorcycle')
        motorcycle_instance = motorcycle('Honda', 'CBR600RR', 2022)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            motorcycle_instance.start()
            motorcycle_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2022 Honda CBR600RR motorcycle.\n"
                                              "Stopping 2022 Honda CBR600RR motorcycle.\n")

    def test_get_non_existent_vehicle(self):
        vehicle = self.VehicleFactory.get('NonExistentVehicle')
        self.assertIsNone(vehicle)


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main(verbosity=1)
