# Caden Kriese - 03-17-2020
"""
API for Infinite Campus courses.
"""

from urllib.parse import urlparse

import requests
from flask import request
from flask_restful import Resource


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


class CoursesAPI(Resource):
    """
    API for listing basic information about all courses of a specific student.
    """

    @staticmethod
    def get():
        """
        Gets a list of all courses.
        :return: All courses the student is currently enrolled in.
        """
        args = request.args
        app_url = args['app_url']
        app_name = args['app_name']
        jsessionid = args['jsessionid']
        app_domain = urlparse(app_url).netloc

        response = requests.get(app_url + 'resources/portal/grades/', cookies={
            'JSESSIONID': jsessionid,
            'appName': app_name,
            'Domain': app_domain
        }).json()

        if 'term' in args:
            index = int(args['term'])
            courses = response[0]['terms'][index]['courses']
        else:
            courses = response[0]['courses']

        # Filter out grading tasks with no detail
        for course in courses:
            if 'gradingTasks' in course:
                course['gradingTasks'] = [task for task in course['gradingTasks']
                                          if 'hasDetail' in task and bool(task['hasDetail'])]

        formatted_courses = [{
            'name': course.get('courseName'),
            'teacher': course.get('teacherDisplay'),
            'letter_grade': get_grade_value(course, 'score'),
            'percent': get_grade_value(course, 'percent')
        } for course in courses]

        return [remove_nulls(course) for course in formatted_courses], 200
