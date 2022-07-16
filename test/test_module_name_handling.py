import os

from unittest import main, TestCase

from cuco import ModuleName


TYPE_SPECIFICATION_ROOT = 'assets/test/types'


class TestModuleNameHandling(TestCase):
    def test_one_component_module_name(self):
        self.assertEqual(ModuleName('foo').get_path(TYPE_SPECIFICATION_ROOT), os.path.join(TYPE_SPECIFICATION_ROOT, 'foo.yml'))

    def test_multicomponent_module_name(self):
        self.assertEqual(ModuleName('foo.bar').get_path(TYPE_SPECIFICATION_ROOT), os.path.join(TYPE_SPECIFICATION_ROOT, 'foo', 'bar.yml'))

    def test_multicomponent_module_name_with_leading_dot(self):
        self.assertEqual(ModuleName('.foo.bar').get_path(TYPE_SPECIFICATION_ROOT), os.path.join(TYPE_SPECIFICATION_ROOT, 'foo', 'bar.yml'))

    def test_module_name_with_one_backstep_component(self):
        self.assertEqual(ModuleName('..foo.bar').get_path(TYPE_SPECIFICATION_ROOT), os.path.join(TYPE_SPECIFICATION_ROOT, '..', 'foo', 'bar.yml'))

    def test_module_name_with_multiple_backstep_components(self):
        self.assertEqual(ModuleName('..foo.bar..baz.qux').get_path(TYPE_SPECIFICATION_ROOT), os.path.join(TYPE_SPECIFICATION_ROOT, '..', 'foo', 'bar', '..', 'baz', 'qux.yml'))

    def test_module_name_with_multipart_backstep_component(self):
        self.assertEqual(ModuleName('....foo.bar').get_path(TYPE_SPECIFICATION_ROOT), os.path.join(TYPE_SPECIFICATION_ROOT, '..', '..', '..', 'foo', 'bar.yml'))

    def test_module_name_with_multiple_multipart_backstep_components(self):
        self.assertEqual(ModuleName('...foo.bar...baz.qux').get_path(TYPE_SPECIFICATION_ROOT), os.path.join(TYPE_SPECIFICATION_ROOT, '..', '..', 'foo', 'bar', '..', '..', 'baz', 'qux.yml'))

    def test_multicomponent_module_name_with_empty_last_part(self):
        self.assertEqual(ModuleName('foo.').get_path(TYPE_SPECIFICATION_ROOT), os.path.join(TYPE_SPECIFICATION_ROOT, 'foo', '.yml'))


if __name__ == "__main__":
    main()
