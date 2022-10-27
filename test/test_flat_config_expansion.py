from unittest import main, TestCase

from cuco.expansion import map_and_expand
from cuco.utils.file import load_yaml


class TestFlatConfigExpansion(TestCase):
    def test_list(self):
        configs = map_and_expand(config = {'foo': ['bar', 'baz']}, mapping = {'foo': 'foo'})
        assert len(configs) == 2

    def test_tuple(self):
        configs = map_and_expand(config = {'foo': ('bar', 'baz')}, mapping = {'foo': 'foo'})
        assert len(configs) == 2

    def test_set(self):
        configs = map_and_expand(config = {'foo': {'bar', 'baz'}}, mapping = {'foo': 'foo'})
        assert len(configs) == 2

    def test_list_without_mapping(self):
        configs = map_and_expand(config = {'foo': ['bar', 'baz']})
        assert len(configs) == 2

    def test_list_which_must_not_be_expanded(self):
        yaml_config = """
        foo:  # as-is
          - bar
          - baz
        """

        configs = map_and_expand(config = load_yaml(string = yaml_config), mapping = {'foo': 'foo'})

        self.assertEqual(len(configs), 1)

    def test_list_which_must_be_expanded_and_list_which_must_not_be_expanded(self):
        yaml_config = """
        aa:
          - bb
          - cc
        foo:  # as-is
          - bar
          - baz
        """

        configs = map_and_expand(config = load_yaml(string = yaml_config), mapping = {'foo': 'foo', 'aa': 'aa'})

        self.assertEqual(len(configs), 2)

    def test_list_which_must_not_be_expanded_with_traling_characters_in_comment(self):
        yaml_config = """
        foo:  # as-is (there must be only one config)
          - bar
          - baz
        """

        configs = map_and_expand(config = load_yaml(string = yaml_config), mapping = {'foo': 'foo'})

        assert len(configs) == 1


if __name__ == "__main__":
    main()
