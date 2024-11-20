import unittest
import config

class TestConfig(unittest.TestCase):

    def test_get_default_path(self):
        config._get_default_path()

    def test_init_config_success(self):
        config._init_config(path='../')

    def test_init_config_failure(self):
        config._init_config(path=None)

    def test_set_parameter(self):
        config.set_parameter('test', 'value')

    def test_set_parameter_numeric(self):
        config.set_parameter('test_number', 661)

    def test_get_parameter_success(self):
        config.set_parameter('test', 'value')
        self.assertEqual('value', config.get_parameter('test'))

    def test_get_parameter_failure(self):
        config.set_parameter('test', 'value')
        self.assertEqual(None, config.get_parameter('test1'))

    def test_convert_to_typed_value_none(self):
        self.assertEqual(None, config.convert_to_typed_value(None))