from unittest import main, TestCase

from test.Foo import Foo
from test.Bar import Bar
from test.Baz import Baz
from test.Corge import Corge
from test.Grault import Grault

from cuco import make_configs


TYPE_SPECIFICATION_ROOT = 'assets/test/types'


class TestConfigObjectCreation(TestCase):
    def test_flat_config_with_two_fields(self):
        configs = make_configs(
            path = 'assets/test/foo/default.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')

    def test_config_with_superclass_and_list_field(self):
        configs = make_configs(
            path = 'assets/test/bar/default.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')

    def test_config_with_custom_object_type_and_field_names(self):
        configs = make_configs(
            path = 'assets/test/qux/default.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')

    def test_config_with_custom_module_name(self):
        configs = make_configs(
            path = 'assets/test/corge/default.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')

    def test_config_with_nested_config_object_instances(self):
        configs = make_configs(
            path = 'assets/test/grault/default.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')
        self.assertEqual(set(config.name for config in configs), {'baz.foo=1', 'baz.foo=2'}, 'Config names do not match')


if __name__ == "__main__":
    main()
