# Caden Kriese - 03-17-2020
"""
API for Infinite Campus courses.
"""

from urllib.parse import urlparse

import requests
from flask import request
from flask_restful import Resource

from server.v1.infinite_campus import infinite_campus as ns


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
                    if index is None:
                        continue
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




class CourseList(Resource):
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
        cookies = request.cookies
        app_url = urlparse(cookies['app_url'])

        response = requests.get(app_url.geturl() + 'resources/portal/grades/', cookies={
            'JSESSIONID': cookies['jsessionid'],
            'appName': cookies['app_name'],
            'Domain': app_url.netloc,
            'campus_hybrid_app': 'student'
        }).json()

        if 'AuthenticationException' in str(response):
            return {'error': 'Invalid Session Token'}, 401

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
            'course_id': course.get('sectionID'),
            'letter_grade': get_grade_value(course, 'score'),
            'percent': get_grade_value(course, 'percent')
        } for course in courses]

        return [remove_nulls(course) for course in formatted_courses], 200


class Course(Resource):
    """
    API for listing detailed information about a specific course.
    """

    @staticmethod
    def get(course_id):
        """
        Gets detailed information from the requested course.
        :return: All courses the student is currently enrolled in.
        """
        cookies = request.cookies
        app_url = urlparse(cookies['app_url'])

        grade_response = requests.get(app_url.geturl() + 'resources/portal/grades/detail/' + course_id, cookies={
            'JSESSIONID': cookies['jsessionid'],
            'appName': cookies['app_name'],
            'Domain': app_url.netloc,
            'campus_hybrid_app': 'student'
        }).json()

        course_response = requests.get(cookies['app_url'] + 'resources/portal/section/' + course_id, params={
            '_expand': 'terms'
        }, cookies={
            'JSESSIONID': cookies['jsessionid'],
            'appName': cookies['app_name'],
            'Domain': app_url.netloc,
            'campus_hybrid_app': 'student',
        }).json()

        if 'AuthenticationException' in str(grade_response) or 'AuthenticationException' in str(course_response):
            return {'error': 'Invalid Session Token'}, 401

        detail = [detail for detail in grade_response['details'] if detail['task'].get('hasDetail')][0]
        task = detail['task']
        categories = detail['categories']

        formatted_courses = {
            'teacher': course_response.get('teacherDisplay'),
            'name': course_response.get('courseName'),
            'number': course_response.get('courseNumber'),
            'task': {
                'name': task.get('taskName'),
                'letter_grade': task.get('score') if 'score' in task else task.get('progressScore'),
                'percentage_grade': task.get('percent') if 'percent' in task else task.get('progressPercent'),
                'categories': [{
                    'name': category.get('name'),
                    'weight': category.get('weight') if 'isWeighted' in category and category['isWeighted'] else None,
                    'excluded': category['isExcluded'] if 'isExcluded' in category and category['isExcluded'] else None,
                    'assignments': [{
                        'name': assignment.get('assignmentName'),
                        'date_due': assignment.get('dueDate'),
                        'date_assigned': assignment.get('assignedDate'),
                        'earned_points': float(assignment['score']) if 'score' in assignment and assignment[
                            'score'] is not None else None,
                        'total_points': float(assignment['totalPoints']) if 'totalPoints' in assignment and assignment[
                            'totalPoints'] is not None else None,
                        'flags': [
                            'late' if assignment.get('late') else None,
                            'missing' if assignment.get('missing') else None,
                            'cheated' if assignment.get('cheated') else None,
                            'dropped' if assignment.get('dropped') else None,
                            'incomplete' if assignment.get('incomplete') else None
                        ]
                    } for assignment in category['assignments']]
                } for category in categories]
            }
        }

        return remove_nulls(formatted_courses), 200
