import os
import re

CAMEL_CASE_TO_KEBAB_CASE_CONVERTING_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')
METADATA_FIELD_PATTERN = re.compile(r'_.+')

YAML_FILE_PATH_PATTERN = re.compile(r'.+\.ya?ml')
YAML_FOLDER_PATH_PATTERN = re.compile(r'@(.+)')

BACKSTEP_MODULE_NAME_COMPONENT_PATTERN = re.compile(r'\.\.+')

LINKED_FIELD_NAME = re.compile(r'\{\{([^}{]+)\}\}')


def camel_case_to_kebab_case(string: str):
    return CAMEL_CASE_TO_KEBAB_CASE_CONVERTING_PATTERN.sub('-', string).lower()


def is_metadata_field(string: str):
    if METADATA_FIELD_PATTERN.fullmatch(string) is None:
        return False
    return True


def is_yaml_file_path(string: str):
    if YAML_FILE_PATH_PATTERN.fullmatch(string) is None:
        return False
    return True


def get_yaml_folder_path(string: str):
    if (match := YAML_FOLDER_PATH_PATTERN.fullmatch(string)) is None:
        return None
    return match.group(1)


def module_name_to_path(name: str):
    backstep_splits = BACKSTEP_MODULE_NAME_COMPONENT_PATTERN.split(name)

    if len(backstep_splits) > 1:
        path_components = [] if (current_backstep_split := backstep_splits[0]) == '' else [current_backstep_split]
        next_backstep_split_index = 1

        for match_ in BACKSTEP_MODULE_NAME_COMPONENT_PATTERN.findall(name):
            path_components.extend('..' for _ in range(len(match_) - 1))
            if (current_backstep_split := backstep_splits[next_backstep_split_index]) != '':
                path_components.extend(current_backstep_split.split('.'))
            next_backstep_split_index += 1
    else:
        path_components = name.split(".")

    return f'{os.path.join(*path_components)}.yml'


def substitute_linked_values(kwargs: dict):
    n_substituted_values = None

    while (n_substituted_values is None or n_substituted_values > 0):
        n_substituted_values = 0
        for key, value in kwargs.items():
            if isinstance(value, str):
                for match_ in LINKED_FIELD_NAME.finditer(value):
                    n_substituted_values += 1
                    field_reference = match_.group(0)
                    field_name = match_.group(1)
                    if (referenced_value := kwargs.get(field_name)) is not None:
                        value = value.replace(field_reference, referenced_value)
            kwargs[key] = value
