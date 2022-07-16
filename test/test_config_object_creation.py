from unittest import main, TestCase

from test.Foo import Foo
from test.Bar import Bar
from test.Baz import Baz

from cuco import make_configs


TYPE_DEFINITION_PATH_PATTERN = 'assets/test/types/{type}.yml'


class TestFlatConfigExpansion(TestCase):
    def test_flat_config_with_two_fields(self):
        configs = make_configs(
            path = 'assets/test/foo/default.yml', type_definition_path_pattern = TYPE_DEFINITION_PATH_PATTERN
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')

    def test_config_with_superclass_and_list_field(self):
        configs = make_configs(
            path = 'assets/test/bar/default.yml', type_definition_path_pattern = TYPE_DEFINITION_PATH_PATTERN
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')

    def test_config_with_custom_object_type_and_field_names(self):
        configs = make_configs(
            path = 'assets/test/qux/default.yml', type_definition_path_pattern = TYPE_DEFINITION_PATH_PATTERN
        )

        self.assertEqual(len(configs), 2, 'Number of generated configs is not correct')


if __name__ == "__main__":
    main()
