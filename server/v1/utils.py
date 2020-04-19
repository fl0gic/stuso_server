# Caden Kriese - 4/13/20
"""
    API Utilities.
"""


def remove_nulls(dictionary):
    """
    Recursively removes all null values from a dict.
    :param dictionary: The dictionary to loop through.
    :return: The same dictionary without any keys with no value.
    """
    new_dict = {}
    for key, val in dictionary.items():
        if val is not None:
            if isinstance(val, dict):
                val = remove_nulls(val)
            elif isinstance(val, list):
                new_list = []
                for index in val:
                    if isinstance(index, dict):
                        index = remove_nulls(index)
                    new_list.append(index)
                val = new_list
            new_dict[key] = val
    return new_dict


def get_grade_value(course, val):
    """
    Gets a specific grade value from a course.
    :param course: The course to get the value from.
    :param val: The key of the value to retrieve.
    :return: The value from the default grading task.
    """
    return course.get('gradingTasks')[0].get(val) if 'gradingTasks' in course \
                                                     and len(course['gradingTasks']) > 0 else None
