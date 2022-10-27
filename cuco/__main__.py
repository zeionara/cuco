from .utils.string import camel_case_to_kebab_case
from .utils.file import read_yaml, load_yaml
from .constants import TYPE_METADATA_FIELD, SELF_METADATA_FIELD, SUPER_METADATA_FIELD, LIST_TYPE, DEFAULT_CONFIG_NAME_KEY
from .expansion import map_and_expand
from .ModuleName import ModuleName
from .exception import InvalidConfigException


object_types = {}
module_names = {}


def handle_nested_type_references(config: dict, root: str):
    items = tuple(config.items())

    for key, value in items:
        if isinstance(value, dict):
            if TYPE_METADATA_FIELD in value:
                assert set(value.keys()) in (
                    {SELF_METADATA_FIELD, TYPE_METADATA_FIELD, SUPER_METADATA_FIELD}, {SELF_METADATA_FIELD, TYPE_METADATA_FIELD}
                ) and (nested_self := value.get(SELF_METADATA_FIELD)) is not None, 'Incorrect field specification'

                nested_type = value[TYPE_METADATA_FIELD]

                if nested_type is not None and nested_type != LIST_TYPE:
                    config[key] = nested_type_specification = read_config_type_specification(nested_type, root = root)
                    nested_type_specification[SELF_METADATA_FIELD] = nested_self
                    nested_type_specification[TYPE_METADATA_FIELD] = nested_type
                    continue

            handle_nested_type_references(value, root = root)

    if (super_type := config.get(SUPER_METADATA_FIELD)):
        for key, value in read_config_type_specification(super_type, root = root).items():
            if key in config:
                # raise ValueError(f'Cannot override key "{key}" - it is specified in both - superclass and subclass')
                continue  # Values in subclasses override values in superclasses
            config[key] = value


def read_config_type_specification(type_: str, root: str):
    assert type_ == LIST_TYPE or (type_ in object_types and type_ in module_names), f'Unknown config object type "{type_}"'

    # path = path_pattern.format(type = type_)
    path = module_names[type_].get_path(root)

    mapping = read_yaml(path)

    handle_nested_type_references(mapping, root = root)

    return mapping


def config_parser(object_type: str = None, module_name: str = None):
    def config_parser_(cls):
        nonlocal object_type, module_name

        if object_type is None:
            object_type = camel_case_to_kebab_case(cls.__name__)

        if object_type in object_types:
            raise ValueError(f'Cannot overwrite config parser for type "{object_type}", the label is already associated with another class')

        if module_name is None:
            module_name = object_type

        object_types[object_type] = cls
        module_names[object_type] = ModuleName(module_name)

        return cls

    return config_parser_


def load(config: dict):  # Initialize classes with given config moving from the deepest object to the top
    config = dict(config)

    if TYPE_METADATA_FIELD not in config:
        # raise ValueError('Cannot obtain target object type from config')
        return config

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


def make_configs(path: str, type_specification_root: str, verbose: bool = False, post_process_config: callable = None, config_name_key: str = DEFAULT_CONFIG_NAME_KEY, **kwargs):
    assert len(kwargs.keys()) < 1 or post_process_config is not None, 'If kwargs are passed, then config post processor must be defined'

    config = load_yaml(path)
    parsed_configs = []

    config_type_specification = read_config_type_specification(config[TYPE_METADATA_FIELD], root = type_specification_root)

    for config in map_and_expand(config, config_type_specification, config_name_key = config_name_key):
        parsed_configs.append(parsed_config := load(config))

        if post_process_config is not None:
            post_process_config(parsed_config, **kwargs)

        if verbose:
            print('parsed config')
            print(config)

    return parsed_configs


def make_config(*args, **kwargs):
    configs = make_configs(*args, **kwargs)

    if (n_configs := len(configs)) != 1:
        raise InvalidConfigException(message = f'There must be generated exactly 1 config, but found {n_configs}')

    return configs[0]
