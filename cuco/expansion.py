from typing import List, Tuple
from dataclasses import dataclass

from .utils.string import is_metadata_field
from .constants import TYPE_METADATA_FIELD, SELF_METADATA_FIELD, LIST_TYPE, DEFAULT_CONFIG_NAME_KEY, SHOULD_NOT_BE_EXPANDED_MARK, SHOULD_BE_EXPANDED_MARK


def should_be_expanded(config: dict, key: str):
    if not hasattr(config, 'ca'):
        return True

    if (meta := config.ca.items.get(key)):
        return meta[2] is None or not meta[2].value.startswith(f'# {SHOULD_NOT_BE_EXPANDED_MARK}')

    return True


def should_not_be_expanded(config: dict, key: str):  # Checks fields with type 'list' for whether they should be expanded or not
    if not hasattr(config, 'ca'):
        return True

    if (meta := config.ca.items.get(key)):
        return meta[2] is None or not meta[2].value.startswith(f'# {SHOULD_BE_EXPANDED_MARK}')

    return True


@dataclass
class ConfigKeyMapping:
    data: dict = None
    prefix: str = None

    def __getitem__(self, key: str):
        if self.data is None:
            return key

        assert key in self.data, f'Unknown mapping for key "{key}"'

        mapped_value = self.data[key]

        if isinstance(mapped_value, dict):
            return mapped_value['_self']
        return mapped_value

    def __contains__(self, key: str):
        return self.data is None or key in self.data

    def get_mapping_of_nested_fields(self, key: str):
        if self.data is None:
            return ConfigKeyMapping(prefix = self.add_prefix(key))

        assert key in self.data, f'Unknown mapping for nested fields associated with key "{key}"'

        return ConfigKeyMapping(data = self.data[key], prefix = self.add_prefix(key))

    def add_prefix(self, key: str):
        return key if ((prefix := self.prefix) is None) else f'{prefix}.{key}'


def _append_field_to_name(config: dict, field: str, key: str, value):
    if (name := config.get(key)) is None:
        config[key] = f'{field}={value}'
    else:
        config[key] = f'{name};{field}={value}'


def _gather_config_names(config: dict, config_names: list = None, config_name_key: str = DEFAULT_CONFIG_NAME_KEY):
    initial_call = False

    if config_names is None:
        config_names = []
        initial_call = True

    items = tuple(config.items())

    for key, value in items:
        if isinstance(value, (list, tuple, set)):
            for item in value:
                if isinstance(item, dict):
                    _gather_config_names(item, config_names, config_name_key = config_name_key)
        elif isinstance(value, dict):
            _gather_config_names(value, config_names, config_name_key = config_name_key)
        elif key == config_name_key:
            config_names.append(value)

    if initial_call:
        config[config_name_key] = ';'.join(config_names)

    return config


def _pop_config_names(config: dict, initial_call: bool = True, config_name_key: str = DEFAULT_CONFIG_NAME_KEY):
    items = tuple(config.items())

    for key, value in items:
        if isinstance(value, (list, tuple, set)):
            for item in value:
                if isinstance(item, dict):
                    _pop_config_names(item, initial_call = False, config_name_key = config_name_key)
        elif isinstance(value, dict):
            _pop_config_names(value, initial_call = False, config_name_key = config_name_key)
        elif key == config_name_key and not initial_call:
            config.pop(config_name_key)

    return config


def _map_and_expand(keys: Tuple[str], configs: List[dict], mapping: ConfigKeyMapping, config_name_key: str):  # , root_config: dict = None):
    if len(keys) < 1:
        return configs

    current_key = keys[0]

    # if mapping is not None:
    if (is_not_metadata_field := not is_metadata_field(current_key)):
        assert current_key in mapping, f'Unknown mapping for key "{current_key}"'
        mapped_key = mapping[current_key]
    else:  # Metadata fields are not changed
        mapped_key = current_key

    updated_configs = []

    for config in configs:
        # print('current config: ', config)
        current_value = config.pop(current_key)
        # print('current key: ', current_key)
        # print('current value: ', current_value)
        # mapped_key = current_key if mapping is None else mapping[current_key]

        if is_not_metadata_field and isinstance(current_value, (list, set, tuple)) and should_be_expanded(config, current_key):
            if mapping.data is not None and (nested_mapping := mapping.data.get(current_key)) is not None and isinstance(nested_mapping, dict): 
                # print(config)
                assert set(nested_mapping.keys()) == {SELF_METADATA_FIELD, TYPE_METADATA_FIELD}, 'Invalid field specification - type definitions corresponding to lists must contain exactly two fields'

                current_value_type = nested_mapping[TYPE_METADATA_FIELD]
                if current_value_type == LIST_TYPE and should_not_be_expanded(config, current_key):
                    current_name_mapping = nested_mapping[SELF_METADATA_FIELD]
                    config[current_name_mapping] = current_value
                    updated_configs.append(dict(config))
                    continue  # It means that property contains list which should not be expanded

            for value in current_value:
                if isinstance(value, dict):
                    # value_copy = dict(value)
                    for value_ in _map_and_expand(
                        sorted(tuple(value.keys())),
                        configs = [value],
                        mapping = mapping.get_mapping_of_nested_fields(current_key),
                        config_name_key = config_name_key
                    ):
                        new_config = config.copy()
                        new_config[mapped_key] = value_
                        updated_configs.append(new_config)
                        # _append_field_to_name(new_config, mapping.add_prefix(current_key), config_name_key, value_copy)  # if root_config is None else root_config
                else:
                    new_config = config.copy()
                    new_config[mapped_key] = value
                    updated_configs.append(new_config)
                    _append_field_to_name(new_config, mapping.add_prefix(current_key), config_name_key, value)  # if root_config is None else root_config
                # print('Root config is')
                # print(root_config)
        elif is_not_metadata_field and isinstance(current_value, dict) and should_be_expanded(config, current_key):
            if TYPE_METADATA_FIELD not in current_value and mapping.data is not None and (nested_mapping := mapping.data.get(current_key)) is not None and TYPE_METADATA_FIELD in nested_mapping: 
                current_value[TYPE_METADATA_FIELD] = nested_mapping[TYPE_METADATA_FIELD]
            # print('making a nested call with root config = ')
            # print(config if root_config is None else root_config)
            # if current_value.get(TYPE_METADATA_FIELD) is None:
            #     config[mapped_key] = current_value  # Do not expand this value
            #     updated_configs.append(config.copy())
            # else:
            for value in _map_and_expand(
                sorted(tuple(current_value.keys())),
                configs = [current_value],
                mapping = mapping.get_mapping_of_nested_fields(current_key),
                config_name_key = config_name_key
                # root_config = config if root_config is None else root_config
            ):
                new_config = config.copy()
                # new_config = config.copy()
                new_config[mapped_key] = value

                updated_configs.append(new_config)
                # _append_field_to_name(new_config, current_key, value)
        else:
            config[mapped_key] = current_value
            updated_configs.append(config.copy())

    return _map_and_expand(keys = keys[1:], configs = updated_configs, mapping = mapping, config_name_key = config_name_key)  # , root_config = root_config)


def map_and_expand(config: dict, mapping: dict = None, config_name_key: str = DEFAULT_CONFIG_NAME_KEY):
    # return _map_and_expand(sorted(tuple(config.keys())), configs = [config], mapping = None if mapping is None else ConfigKeyMapping(data = mapping))
    configs = _map_and_expand(sorted(tuple(config.keys())), configs = [config], mapping = ConfigKeyMapping(data = mapping), config_name_key = config_name_key)

    for config_ in configs:
        _gather_config_names(config_, config_name_key = config_name_key)

    for config_ in configs:
        _pop_config_names(config_, config_name_key = config_name_key)

    return configs


def try_pop(values: dict, key, default = None):
    if key in values:
        return values.pop(key)
    return default
