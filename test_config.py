import unittest
import config

class TestArgs:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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
        self.assertEqual(None, config.get_parameter('test1'))

    def test_get_parameter_default(self):
        self.assertEqual(33, config.get_parameter('test1', 33))

    def test_convert_to_typed_value_none(self):
        self.assertEqual(None, config.convert_to_typed_value(None))

    def test_convert_to_typed_value_not_str(self):
        self.assertEqual(12345, config.convert_to_typed_value(12345))
    
    def test_overwrite_from_args(self):
        args = TestArgs(param1='value1', param2=None, param3=100)
        config.overwrite_from_args(args)
        self.assertEqual(config.get_parameter('param1'), 'value1')
        self.assertEqual(config.get_parameter('param3'), 100)
        self.assertIsNone(config.get_parameter('param2'))
