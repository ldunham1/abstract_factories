import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Monkeypatch python 2.7 unittest.TestCase.
if sys.version_info[0] == 2:
    unittest.TestCase.assertCountEqual = unittest.TestCase.assertItemsEqual

from abstract_factories import AbstractTypeFactory, AbstractInstanceFactory


class MockAbstract(object):
    Name = ''


class MockItem1(MockAbstract):
    Name = 'MockItem1'


class MockItem2(MockAbstract):
    Name = 'MockItem2'
    Version = 1.0


class MockItem2b(MockItem2):
    Version = 2.0


class MockItem2c(MockItem2):
    Version = 3.0


# ------------------------------------------------------------------------------
class TestCallableIdentifierFactories(unittest.TestCase):

    def test_callable_name_key(self):
        def get_name(item):
            return item.Name

        factory = AbstractTypeFactory(MockAbstract, name_key=get_name)
        factory.register_item(MockItem1)
        self.assertEqual(factory.get_name(MockItem1), 'MockItem1')

    def test_callable_version_key(self):
        def get_version(item):
            return item.Version

        factory = AbstractTypeFactory(MockAbstract, name_key='Name', version_key=get_version)
        factory.register_item(MockItem2)
        self.assertEqual(factory.get_version(MockItem2), 1.0)

    def test_callable_keys(self):
        factory = AbstractTypeFactory(MockAbstract, name_key=lambda item: item.Name, version_key=lambda item: item.Version)
        factory.register_item(MockItem2)
        self.assertEqual(factory.get_name(MockItem2), 'MockItem2')
        self.assertEqual(factory.get_version(MockItem2), 1.0)


# ------------------------------------------------------------------------------
class TestTypeFactoryItems(unittest.TestCase):

    def setUp(self):
        self.factory = AbstractTypeFactory(MockAbstract, name_key='Name', version_key='Version')

    def test_init(self):
        self.assertIsInstance(self.factory, AbstractTypeFactory)
        self.assertEqual(self.factory.abstract, MockAbstract)
        self.assertEqual(len(self.factory.items()), 0)

    def test_factory_str(self):
        self.assertEqual(str(self.factory), "AbstractTypeFactory(items=0)")

    def test_private__is_viable_item(self):
        self.assertFalse(self.factory._is_viable_item(object()))
        self.assertFalse(self.factory._is_viable_item(MockAbstract))  # Abstract itself should not be viable.
        self.assertTrue(self.factory._is_viable_item(MockItem1))

    def test_register_item(self):
        self.assertTrue(self.factory.register_item(MockItem1))
        self.assertEqual(len(self.factory.items()), 1)

    def test_register_wrong_item_type(self):
        instance = MockItem1()
        self.assertFalse(self.factory.register_item(instance))
        self.assertEqual(len(self.factory.items()), 0)

    def test_deregister_item(self):
        self.factory.register_item(MockItem1)
        self.assertTrue(self.factory.deregister_item(MockItem1))
        self.assertEqual(len(self.factory.items()), 0)

    def test_register_duplicate_item(self):
        self.assertTrue(self.factory.register_item(MockItem1))
        self.assertFalse(self.factory.register_item(MockItem1))
        self.assertEqual(len(self.factory.items()), 1)

    def test_get_name(self):
        self.factory.register_item(MockItem1)
        self.assertEqual(self.factory.get_name(MockItem1), 'MockItem1')

    def test_get_version(self):
        self.factory.register_item(MockItem2)
        self.assertEqual(self.factory.get_version(MockItem2), 1.0)

    def test_get(self):
        self.factory.register_item(MockItem2b)
        self.factory.register_item(MockItem2)
        self.factory.register_item(MockItem2c)

        self.assertEqual(self.factory.get('MockItem2', version=1.0), MockItem2)
        self.assertEqual(self.factory.get('MockItem2', version=2.0), MockItem2b)
        self.assertEqual(self.factory.get('MockItem2', version=3.0), MockItem2c)

    def test_get_latest_version(self):
        self.factory.register_item(MockItem2)
        self.factory.register_item(MockItem2c)
        self.factory.register_item(MockItem2b)

        self.assertEqual(self.factory.get('MockItem2'), MockItem2c)

    def test_names(self):
        self.factory.register_item(MockItem1)
        self.factory.register_item(MockItem2)

        self.assertCountEqual(self.factory.names(), ['MockItem1', 'MockItem2'])

    def test_names_versions(self):
        self.factory.register_item(MockItem1)
        self.factory.register_item(MockItem2)
        self.factory.register_item(MockItem2b)
        self.factory.register_item(MockItem2c)

        self.assertCountEqual(self.factory.names(), ['MockItem1', 'MockItem2'])

    def test_versions(self):
        self.factory.register_item(MockItem2)
        self.factory.register_item(MockItem2c)
        self.factory.register_item(MockItem2b)

        self.assertListEqual(self.factory.versions('MockItem2'), [1.0, 2.0, 3.0])

    def test_items(self):
        self.factory.register_item(MockItem1)
        self.factory.register_item(MockItem2)

        self.assertCountEqual(self.factory.items(), [MockItem1, MockItem2])

    def test_clear(self):
        self.factory.register_item(MockItem1)
        self.factory.clear()
        self.assertEqual(len(self.factory.items()), 0)


# ------------------------------------------------------------------------------
class TestInstanceFactoryItems(unittest.TestCase):

    def setUp(self):
        self.factory = AbstractInstanceFactory(MockAbstract, name_key='Name', version_key='Version')

    def test_init(self):
        self.assertIsInstance(self.factory, AbstractInstanceFactory)
        self.assertEqual(self.factory.abstract, MockAbstract)
        self.assertEqual(len(self.factory.items()), 0)

    def test_factory_str(self):
        self.assertEqual(str(self.factory), "AbstractInstanceFactory(items=0)")

    def test_private__is_viable_item(self):
        self.assertFalse(self.factory._is_viable_item(object()))
        self.assertFalse(self.factory._is_viable_item(MockAbstract()))  # Abstract itself should not be viable.
        self.assertTrue(self.factory._is_viable_item(MockItem1()))

    def test_register_item(self):
        instance = MockItem1()
        self.assertTrue(self.factory.register_item(instance))
        self.assertEqual(len(self.factory.items()), 1)

    def test_register_wrong_item_type(self):
        self.assertFalse(self.factory.register_item(MockItem1))
        self.assertEqual(len(self.factory.items()), 0)

    def test_deregister_item(self):
        instance = MockItem1()
        self.factory.register_item(instance)
        self.assertTrue(self.factory.deregister_item(instance))
        self.assertEqual(len(self.factory.items()), 0)

    def test_register_duplicate_item(self):
        instance = MockItem1()
        self.assertTrue(self.factory.register_item(instance))
        self.assertFalse(self.factory.register_item(instance))
        self.assertEqual(len(self.factory.items()), 1)

    def test_get_name(self):
        instance = MockItem1()
        self.factory.register_item(instance)
        self.assertEqual(self.factory.get_name(instance), 'MockItem1')

    def test_get_version(self):
        instance = MockItem2()
        self.factory.register_item(instance)
        self.assertEqual(self.factory.get_version(instance), 1.0)

    def test_get_latest_version(self):
        instance1 = MockItem2()
        instance2 = MockItem2()
        instance2.Version = 2.0  # Modify the instance.Version attribute
        instance3 = MockItem2c()

        self.factory.register_item(instance1)
        self.factory.register_item(instance3)
        self.factory.register_item(instance2)

        self.assertEqual(self.factory.get('MockItem2'), instance3)
        self.assertEqual(self.factory.get('MockItem2', version=None), instance3)

    def test_get(self):
        instance1 = MockItem2()
        instance2 = MockItem2()
        instance2.Version = 2.0  # Modify the instance.Version attribute
        instance3 = MockItem2c()

        self.factory.register_item(instance1)
        self.factory.register_item(instance3)
        self.factory.register_item(instance2)

        self.assertEqual(self.factory.get('MockItem2', version=1.0), instance1)
        self.assertEqual(self.factory.get('MockItem2', version=2.0), instance2)
        self.assertEqual(self.factory.get('MockItem2', version=3.0), instance3)

    def test_names(self):
        instance1 = MockItem1()
        instance2 = MockItem2()
        self.factory.register_item(instance1)
        self.factory.register_item(instance2)

        self.assertCountEqual(self.factory.names(), ['MockItem1', 'MockItem2'])

    def test_names_versions(self):
        instance1 = MockItem1()
        instance2 = MockItem2()
        instance2b = MockItem2b()
        instance2c = MockItem2c()
        self.factory.register_item(instance1)
        self.factory.register_item(instance2)
        self.factory.register_item(instance2b)
        self.factory.register_item(instance2c)

        self.assertCountEqual(self.factory.names(), ['MockItem1', 'MockItem2'])

    def test_versions(self):
        instance1 = MockItem2()
        instance2 = MockItem2()
        instance2.Version = 2.0  # Modify the instance.Version attribute
        instance3 = MockItem2c()
        self.factory.register_item(instance1)
        self.factory.register_item(instance2)
        self.factory.register_item(instance3)

        self.assertListEqual(self.factory.versions('MockItem2'), [1.0, 2.0, 3.0])

    def test_items(self):
        instance1 = MockItem1()
        instance2 = MockItem2()
        instance3 = MockItem2c()
        self.factory.register_item(instance1)
        self.factory.register_item(instance2)
        self.factory.register_item(instance3)

        self.assertCountEqual(self.factory.items(), [instance1, instance2, instance3])

    def test_clear(self):
        instance1 = MockItem1()
        self.factory.register_item(instance1)
        self.factory.clear()
        self.assertEqual(len(self.factory.items()), 0)


# ------------------------------------------------------------------------------
class TestMultiTypeFactoryItems(TestTypeFactoryItems):

    def setUp(self):
        self.factory = AbstractTypeFactory(
            MockAbstract,
            name_key='Name',
            version_key='Version',
            unique_items_only=False,
        )

    def test_register_duplicate_item(self):
        self.assertTrue(self.factory.register_item(MockItem1))
        self.assertTrue(self.factory.register_item(MockItem1))
        self.assertEqual(len(self.factory.items()), 2)


# ------------------------------------------------------------------------------
class TestMultiInstanceFactoryItems(TestInstanceFactoryItems):

    def setUp(self):
        self.factory = AbstractInstanceFactory(
            MockAbstract,
            name_key='Name',
            version_key='Version',
            unique_items_only=False,
        )

    def test_register_duplicate_item(self):
        instance = MockItem1()
        self.assertTrue(self.factory.register_item(instance))
        self.assertTrue(self.factory.register_item(instance))
        self.assertEqual(len(self.factory.items()), 2)


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main(verbosity=1)
