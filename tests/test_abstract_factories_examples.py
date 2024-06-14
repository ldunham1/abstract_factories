import os
import sys
import unittest

# Monkeypatch python 2.7 unittest.TestCase.
if sys.version_info[0] == 2:
    unittest.TestCase.assertCountEqual = unittest.TestCase.assertItemsEqual

root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'examples'))

from simple_validation import DataValidator
from rig_factory import RigComponentBuilder


# ------------------------------------------------------------------------------
class TestExampleJsonValidator(unittest.TestCase):

    def setUp(self):
        self.Validator = DataValidator()

    def test_init(self):
        """Test validator has initialized."""
        self.assertIsNotNone(self.Validator)

    def test_collection(self):
        """Test context collection succeeds."""
        json_root = os.path.join(root_dir, 'examples', 'simple_validation', '_resources')
        data_list = list(self.Validator.collect(path=json_root))
        self.assertGreaterEqual(len(data_list), 2)

    def test_validation(self):
        """Test validation success and failures."""
        json_root = os.path.join(root_dir, 'examples', 'simple_validation', '_resources')
        data_list = list(self.Validator.collect(path=json_root))
        results = self.Validator.validate(data_list)
        self.assertEqual(results, {'Context("invalid_json_file.json")': {'JsonFileValidator()': ['No json data deserialized.']}})


# ------------------------------------------------------------------------------
class TestExampleRigBuilder(unittest.TestCase):

    def setUp(self):
        self.Builder = RigComponentBuilder()

    def test_init(self):
        """Test builder has initialized."""
        self.assertIsNotNone(self.Builder)

    def test_build(self):
        """Test builder creates correct component instances."""
        build_data = [
            {'type': 'IKChainComponent', 'name': 'arm'},
            {'type': 'IKChainComponent', 'name': 'leg', 'version': 1},
        ]
        components = self.Builder.build(build_data)
        self.assertEqual(len(components), 2)
        self.assertCountEqual([str(comp) for comp in components], ['IKChainComponent(v=2)', 'IKChainComponent(v=1)'])


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main(verbosity=1)
