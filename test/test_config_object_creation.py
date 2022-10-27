from unittest import main, TestCase

from test.Foo import Foo
from test.Bar import Bar
from test.Baz import Baz
from test.Corge import Corge
from test.Grault import Grault
from test.Garply import Garply

from cuco import make_config, make_configs, InvalidConfigException


TYPE_SPECIFICATION_ROOT = 'assets/test/types'


class TestConfigObjectCreation(TestCase):
    def test_flat_config_with_two_fields_using_method_for_single_config_creation_with_invalid_file(self):
        with self.assertRaises(InvalidConfigException):
            make_config(
                path = 'assets/test/foo/default.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
            )

    def test_flat_config_with_two_fields_using_method_for_single_config_creation(self):
        config = make_config(
            path = 'assets/test/foo/single.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )
        
        self.assertEqual((config.foo, config.bar, config.name), (17, 'baz', ''), 'Generated config contains invalid values')

    def test_flat_config_with_two_fields(self):
        configs = make_configs(
            path = 'assets/test/foo/default.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')

    def test_flat_config_with_two_fields_and_custom_name_prefix(self):
        configs = make_configs(
            path = 'assets/test/foo/custom-name-prefix.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual([config.name for config in configs], ['custom;foo=17', 'custom;foo=18'])

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')

    def test_config_with_superclass_and_list_field(self):
        configs = make_configs(
            path = 'assets/test/bar/default.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')

    def test_config_with_superclass_and_list_field_with_forced_expansion(self):
        configs = make_configs(
            path = 'assets/test/bar/force-expand-list-field.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual(len(configs), 4, 'Number of generated configs is not correct')

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

    def test_config_with_linked_values(self):
        configs = make_configs(
            path = 'assets/test/garply/default.yml', type_specification_root = TYPE_SPECIFICATION_ROOT
        )

        self.assertEqual(configs[0].bar, 'garplywaldo', 'Linked values are handled incorrectly')


if __name__ == "__main__":
    main()
