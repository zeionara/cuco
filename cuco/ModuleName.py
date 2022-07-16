import os

from .utils.string import module_name_to_path


class ModuleName:
    def __init__(self, value: str):
        self.value = value
        self._path = None

    @property
    def path(self):
        if self._path is None:
            self._path = module_name_to_path(self.value)
        return self._path

    def get_path(self, root: str):
        return os.path.join(root, self.path)
