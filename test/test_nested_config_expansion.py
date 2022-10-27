from unittest import main, TestCase

from cuco.expansion import map_and_expand
from cuco.utils.file import load_yaml


class TestNestedConfigExpansion(TestCase):
    def test_list(self):
        configs = map_and_expand(config = {'foo': {'bar': ['baz', 'qux']}}, mapping = {'foo': {'_self': 'foo', 'bar': 'bar'}})
        assert len(configs) == 2

    def test_list_without_mapping(self):
        configs = map_and_expand(config = {'foo': {'bar': ['baz', 'qux']}})
        assert len(configs) == 2

    def test_nested_field_which_must_not_be_expanded(self):
        yaml_config = """
        foo:
          bar:  # as-is
            baz:
              - qux
              - quux
        """

        configs = map_and_expand(config = load_yaml(string = yaml_config))

        assert len(configs) == 1

    def test_nested_field_which_must_expanded(self):
        yaml_config = """
        foo:
          bar:
            baz:
              - qux
              - quux
        """

        configs = map_and_expand(config = load_yaml(string = yaml_config))

        assert len(configs) == 2

    def test_nested_list_which_must_not_be_expanded(self):
        yaml_config = """

        foo:
          bar: # as-is
            - bar
            - baz
        """

        configs = map_and_expand(config = load_yaml(string = yaml_config), mapping = {'foo': {'_self': 'bar', 'bar': 'bar'}})

        assert len(configs) == 1


if __name__ == "__main__":
    main()
