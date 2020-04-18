# Caden Kriese - 04-10-2020
"""
Utilities for response filtering.
"""


def apply_mapping(response, mapping):
    """
    Applies mapping to a dictionary.
    :param response: The dictionary or list of dictionaries to be mapped.
    :param mapping: The mappings of the dictionary.
        This should be a dictionary with the correct identifier as a string key,
        and the value as a tuple of the previous identifier and the type.
    :return: 
    """
    if isinstance(response, list):
        result = [apply_mapping(val, mapping) for val in response]
    elif isinstance(response, dict):
        result = {}
        for name, spec in mapping.items():
            value = response.get(spec[0])
            if len(spec) > 1 and value is not None:
                element_type = spec[1]
                if element_type == dict:
                    result[name] = apply_mapping(value, spec[2])
                elif element_type == list and len(spec > 2):
                    result[name] = [apply_mapping(v, spec[2]) for v in list(value)]
                else:
                    result[name] = element_type(value)
            else:
                result[name] = value
    else:
        raise TypeError('Invalid type {} given to mapping, must be list or dict.'.format(type(response)))

    return result
