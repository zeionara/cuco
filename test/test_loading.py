from unittest import main, TestCase

from cuco.utils.file import load_yaml


class TestLoading(TestCase):
    def test_single_file_config(self):
        self.assertEqual(load_yaml('assets/test/single-file.yml'), {'foo': {'bar': {'baz': ['qux', 'quux']}}})

    def test_config_with_another_file_reference(self):
        self.assertEqual(load_yaml('assets/test/multiple-files/foo.yml'), {'foo': {'bar': {'baz': ['qux', 'quux']}}})

    def test_stringified_config_with_another_file_reference(self):
        self.assertEqual(
            load_yaml(
                string = """
                foo:
                  bar: assets/test/multiple-files/baz.yml
                """
            ),
            {'foo': {'bar': {'baz': ['qux', 'quux']}}}
        )

    def test_config_with_folder_reference(self):
        self.assertEqual(load_yaml('assets/test/single-folder/foo.yml'), {'foo': {'bar': {'baz': [{'qux': 'quux'}]}}})

    def test_config_with_nested_folders(self):
        self.assertEqual(load_yaml('assets/test/nested-folders/foo.yml'), {'foo': {'bar': {'baz': [[{'quux': 'corge'}]]}}})


if __name__ == "__main__":
    main()
