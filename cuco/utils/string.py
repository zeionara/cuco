import re

CAMEL_CASE_TO_KEBAB_CASE_CONVERTING_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')
METADATA_FIELD_PATTERN = re.compile(r'_.+')

YAML_FILE_PATH_PATTERN = re.compile(r'.+\.ya?ml')
YAML_FOLDER_PATH_PATTERN = re.compile(r'@(.+)')


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
