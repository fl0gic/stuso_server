# Caden Kriese - 04-10-2020
"""
Utilities for applying mappings to dictionaries.
"""


class BaseMapping(object):
    def __init__(self, old_name=None, new_name=None, get_lambda=None, format_lambda=None):
        self.get_lambda = get_lambda
        self.format_lambda = format_lambda
        self.new_name = new_name
        self.old_name = old_name


class NestedMapping(BaseMapping):
    def __init__(self, mappings=None, **kwargs):
        self.mapping = mappings
        super(NestedMapping, self).__init__(**kwargs)


class NestedListMapping(BaseMapping):
    def __init__(self, mappings=None, **kwargs):
        self.mapping = mappings
        super(NestedListMapping, self).__init__(**kwargs)


def apply_mapping(to_map, maps):
    """
    Applies mapping to a dictionary.
    :param to_map: The dictionary or list of dictionaries to be mapped.
    :param maps: The mappings of the dictionary. This should be a list of BaseMappings/NestedMappings.
    :return: The mapped dictionary.
    """
    if isinstance(to_map, list):
        result = [apply_mapping(val, maps) for val in to_map]
    elif isinstance(to_map, dict):
        result = {}
        for mapping in maps:
            if mapping.old_name is None or mapping.get_lambda is not None:
                value = mapping.get_lambda(to_map)
            else:
                value = to_map.get(mapping.old_name)

            if value is None:
                result[mapping.new_name] = None
                continue

            if mapping.format_lambda is not None:
                value = mapping.format_lambda(value)

            if isinstance(mapping, NestedMapping):
                result[mapping.new_name] = apply_mapping(value, mapping.mapping)
            elif isinstance(mapping, NestedListMapping):
                result[mapping.new_name] = [apply_mapping(v, mapping.mapping) for v in value]
            else:
                result[mapping.new_name] = value
    else:
        raise TypeError('Invalid type {} given to mapping, must be list or dict.'.format(type(to_map)))

    return result
