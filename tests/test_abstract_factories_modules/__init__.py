from unittest.mock import patch
import os
import sys
import unittest


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from . import vehicles
from .abstract import VehicleAbstract
from abstract_factories import AbstractTypeFactory, AbstractInstanceFactory

try:
    from io import StringIO
except ImportError:
    from unittest.mock import StringIO


# ------------------------------------------------------------------------------
class TestVehicleTypeFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.VehicleFactory = AbstractTypeFactory(VehicleAbstract, modules=[vehicles])

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

    def test_get_jetski(self):
        jetski = self.VehicleFactory.get('JetSki')
        self.assertIsNone(jetski)

    def test_get_non_existent_vehicle(self):
        vehicle = self.VehicleFactory.get('NonExistentVehicle')
        self.assertIsNone(vehicle)


class TestVehicleRecursiveTypeFactory(TestVehicleTypeFactory):

    @classmethod
    def setUpClass(cls):
        cls.VehicleFactory = AbstractTypeFactory(VehicleAbstract)
        cls.VehicleFactory.register_module(vehicles, recursive=True)

    def test_get_jetski(self):
        jetski = self.VehicleFactory.get('JetSki')
        jetski_instance = jetski('Kawasaki', 'Ultra LX', 2021)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            jetski_instance.start()
            jetski_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2021 Kawasaki Ultra LX jetski.\n"
                                              "Stopping 2021 Kawasaki Ultra LX jetski.\n")

    def test_get_horse(self):
        horse = self.VehicleFactory.get('Horse')
        horse_instance = horse('Arabian', 'Bay', 2021)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            horse_instance.start()
            horse_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2021 Arabian Bay horse.\n"
                                              "Stopping 2021 Arabian Bay horse.\n")


# ------------------------------------------------------------------------------
class TestVehicleInstanceFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.VehicleFactory = AbstractInstanceFactory(
            VehicleAbstract,
            modules=[vehicles],
            name_key='name',
            version_key='year',
        )

    def test_get_car(self):
        car_instance = self.VehicleFactory.get('Ford Fiesta')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            car_instance.start()
            car_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 1987 Ford Fiesta car.\n"
                                              "Stopping 1987 Ford Fiesta car.\n")

    def test_get_truck(self):
        truck_instance = self.VehicleFactory.get('Ford F-150')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            truck_instance.start()
            truck_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2020 Ford F-150 truck.\n"
                                              "About to stop...\n"
                                              "Stopping 2020 Ford F-150 truck.\n")

    def test_get_truck_alt_version(self):
        truck_instance = self.VehicleFactory.get('Ford F-150', version=2018)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            truck_instance.start()
            truck_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2018 Ford F-150 truck.\n"
                                              "Stopping 2018 Ford F-150 truck.\n")

    def test_get_motorcycle(self):
        motorcycle_instance = self.VehicleFactory.get('Yamaha R3')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            motorcycle_instance.start()
            motorcycle_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2012 Yamaha R3 motorcycle.\n"
                                              "Stopping 2012 Yamaha R3 motorcycle.\n")

    def test_get_motorcycles(self):
        for name in ['Yamaha R3', 'Honda CBR']:
            motorcycle_instance = self.VehicleFactory.get(name)
            self.assertTrue(motorcycle_instance)

    def test_get_jetski(self):
        jetski_instance = self.VehicleFactory.get('Kawasaki Ultra LX')
        self.assertIsNone(jetski_instance)

    def test_get_non_existent_vehicle(self):
        vehicle = self.VehicleFactory.get('NonExistentVehicle')
        self.assertIsNone(vehicle)


class TestVehicleRecursiveInstanceFactory(TestVehicleInstanceFactory):

    @classmethod
    def setUpClass(cls):
        cls.VehicleFactory = AbstractInstanceFactory(
            VehicleAbstract,
            name_key='name',
            version_key='year',
        )
        cls.VehicleFactory.register_module(vehicles, recursive=True)

    def test_get_jetski(self):
        jetski_instance = self.VehicleFactory.get('Kawasaki Ultra LX')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            jetski_instance.start()
            jetski_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 2021 Kawasaki Ultra LX jetski.\n"
                                              "Stopping 2021 Kawasaki Ultra LX jetski.\n")

    def test_get_horse(self):
        horse_instance = self.VehicleFactory.get('Coconuts Brown')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            horse_instance.start()
            horse_instance.stop()
        self.assertEqual(fake_out.getvalue(), "Starting 1975 Coconuts Brown horse.\n"
                                              "Stopping 1975 Coconuts Brown horse.\n")


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main(verbosity=1)
