from .utils.string import camel_case_to_kebab_case
from .utils.file import read_yaml, load_yaml
from .constants import TYPE_METADATA_FIELD, SELF_METADATA_FIELD, SUPER_METADATA_FIELD, LIST_TYPE, DEFAULT_CONFIG_NAME_KEY
from .expansion import map_and_expand


object_types = {}


def handle_nested_type_references(config: dict, path_pattern: str):
    items = tuple(config.items())

    for key, value in items:
        if isinstance(value, dict):
            if TYPE_METADATA_FIELD in value:
                assert set(value.keys()) in (
                    {SELF_METADATA_FIELD, TYPE_METADATA_FIELD, SUPER_METADATA_FIELD}, {SELF_METADATA_FIELD, TYPE_METADATA_FIELD}
                ) and (nested_self := value.get(SELF_METADATA_FIELD)) is not None, 'Incorrect field specification'

                nested_type = value[TYPE_METADATA_FIELD]

                if nested_type is not None and nested_type != LIST_TYPE:
                    config[key] = nested_type_specification = read_config_type_specification(nested_type, path_pattern = path_pattern)
                    nested_type_specification[SELF_METADATA_FIELD] = nested_self
                    nested_type_specification[TYPE_METADATA_FIELD] = nested_type
                    continue

            handle_nested_type_references(value, path_pattern = path_pattern)

    if (super_type := config.get(SUPER_METADATA_FIELD)):
        for key, value in read_config_type_specification(super_type, path_pattern = path_pattern).items():
            if key in config:
                # raise ValueError(f'Cannot override key "{key}" - it is specified in both - superclass and subclass')
                continue  # Values in subclasses override values in superclasses
            config[key] = value


def read_config_type_specification(type_: str, path_pattern: str):
    assert type_ == LIST_TYPE or type_ in object_types, f'Unknown config object type "{type_}"'

    path = path_pattern.format(type = type_)

    mapping = read_yaml(path)

    handle_nested_type_references(mapping, path_pattern = path_pattern)

    return mapping


def config_parser(object_type: str = None):
    def config_parser_(cls):
        nonlocal object_type

        if object_type is None:
            object_type = camel_case_to_kebab_case(cls.__name__)

        object_types[object_type] = cls

        return cls

    return config_parser_


def load(config: dict):  # Initialize classes with given config moving from the deepest object to the top
    config = dict(config)

    if TYPE_METADATA_FIELD not in config:
        raise ValueError('Cannot obtain target object type from config')

    object_type = config[TYPE_METADATA_FIELD]

    config.pop(TYPE_METADATA_FIELD)

    if object_type is not None and (target_class := object_types.get(object_type)) is None:
        raise ValueError(f'No class registered for parsing config as an instance of "{object_type}"')

    for key, value in config.items():
        if isinstance(value, (list, tuple, set)) and any(isinstance(item, dict) for item in value):
            config[key] = type(value)(load(item) if isinstance(item, dict) else item for item in value)
        elif isinstance(value, dict):
            config[key] = load(value)

    parsed_config = config if object_type is None else target_class.load(**config)

    return parsed_config


def make_configs(path: str, type_definition_path_pattern: str, verbose: bool = False, post_process_config: callable = None, config_name_key: str = DEFAULT_CONFIG_NAME_KEY, **kwargs):
    assert len(kwargs.keys()) < 1 or post_process_config is not None, 'If kwargs are passed, then config post processor must be defined'

    config = load_yaml(path)
    parsed_configs = []

    config_type_specification = read_config_type_specification(config[TYPE_METADATA_FIELD], path_pattern = type_definition_path_pattern)

    for config in map_and_expand(config, config_type_specification, config_name_key = config_name_key):
        parsed_configs.append(parsed_config := load(config))

        post_process_config(parsed_config, **kwargs)

        if verbose:
            print('parsed config')
            print(config)

    return parsed_configs
