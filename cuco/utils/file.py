import os
from pathlib import Path

from yaml import safe_load
import ruamel.yaml

from .string import is_yaml_file_path, get_yaml_folder_path


def read_yaml(path: str):
    with open(path, 'r', encoding = 'utf-8') as file:
        return safe_load(file)


yaml = ruamel.yaml.YAML()


def read_referenced_folder(path: str = None):
    items = []

    for item in os.listdir(path):
        if os.path.isfile(current_path := os.path.join(path, item)) and is_yaml_file_path(current_path):
            items.append(load_yaml(current_path))
        elif os.path.isdir(current_path):
            items.append(read_referenced_folder(current_path))

    return items


def read_referenced_file(value: str, path: str = None):
    if isinstance(value, str):
        if is_yaml_file_path(value):
            nested_config = load_yaml(value if path is None else os.path.join(path, value))
            read_referenced_files(nested_config, path = Path(value).parent if path is None else os.path.join(path, Path(value).parent))
            return nested_config
        if (folder_path := get_yaml_folder_path(value)) is not None:
            return read_referenced_folder(path = os.path.join(folder_path if path is None else os.path.join(path, folder_path)))
        return value

    if isinstance(value, dict):
        read_referenced_files(value, path = path)

    return value


def read_referenced_files(config: dict, path: str = None):
    items = tuple(config.items())

    for key, value in items:
        if isinstance(value, (set, list, tuple)):
            config[key] = [
                read_referenced_file(item, path)
                for item in value
            ]
        else:
            config[key] = read_referenced_file(value, path)

        # if isinstance(value, str):
        #     if is_yaml_file_path(value):
        #         config[key] = nested_config = load_yaml(value if path is None else os.path.join(path, value))
        #         read_referenced_files(nested_config, path = Path(value).parent if path is None else os.path.join(path, Path(value).parent))
        #     elif (folder_path := get_yaml_folder_path(value)) is not None:
        #         config[key] = read_referenced_folder(path = os.path.join(folder_path if path is None else os.path.join(path, folder_path)))
        # elif isinstance(value, dict):
        #     read_referenced_files(value, path = path)


def load_yaml(path: str = None, string: str = None):
    assert string is None and path is not None or string is not None and path is None, 'Either path to an external file either string must be provided'

    if path is None:
        content = string
    else:
        with open(path, 'r', encoding = 'utf-8') as file:
            content = file.read()

    config = yaml.load(content)

    read_referenced_files(config, path = None if path is None else Path(path).parent)

    return config
