# Caden Kriese - 03-17-2020
"""
API for Infinite Campus courses.
"""
from urllib.parse import urlparse

import requests
from flask_restx import Namespace, Resource, reqparse, abort

from .models import *
from ..utils.mapping import *

ns = Namespace('infinitecampus', path='/ic',
               description='API requests for grabbing data specifically from Infinite Campus.')

req_args = reqparse.RequestParser()
# Infinite Campus Cookies
req_args.add_argument('JSESSIONID', type=str, required=True, help='The session id cannot be blank!', location='cookies')
req_args.add_argument('app_url', type=str, required=True, help='The app base URL cannot be blank!', location='cookies')
req_args.add_argument('app_name', type=str, required=True, help='The app name cannot be blank!', location='cookies')
# Other Args
req_args.add_argument('term', type=int, help='Term must be an int!', location='args')


def get_grading_task_field(grading_tasks, field, alternate_field):
    """
    Get a field from the primary grading task.
    :param grading_tasks: The list of grading tasks.
    :param field: The name of the field to get.
    :param alternate_field: An alternate name for the field if the first one does not exist.
    :return: The value of the field.
    """
    if grading_tasks is None:
        return None
    tasks = [task for task in grading_tasks if task['hasDetail']]
    if 0 == len(tasks):
        return None
    tasks = tasks[0]
    if field in tasks:
        return tasks.get(field)
    else:
        return tasks.get(alternate_field)


def generate_flags(dct):
    """
    Generates flag list from a map.
    :param dct: The dictionary to retrieve the flags from.
    :return: A list of assignment flags.
    """
    flags = ['late', 'missing', 'cheated', 'dropped', 'incomplete']
    flags = [f for f in flags if f not in dct or dct[f]]
    return flags


assignment_mapping = [
    BaseMapping(old_name='assignmentName', new_name='name'),
    BaseMapping(old_name='dueDate', new_name='date_due'),
    BaseMapping(old_name='assignedDate', new_name='date_assigned'),
    BaseMapping(old_name='scorePoints', new_name='points_earned', format_lambda=float),
    BaseMapping(old_name='totalPoints', new_name='points_total', format_lambda=float),
    BaseMapping(get_lambda=lambda mp: generate_flags(mp), new_name='flags'),
]

grade_category_mapping = [
    BaseMapping(old_name='name', new_name='name'),
    BaseMapping(old_name='weight', new_name='weight'),
    BaseMapping(get_lambda=lambda mp: mp['isExcluded'] if 'isExcluded' in mp and mp['isExcluded'] else None,
                new_name='excluded'),
    BaseMapping(get_lambda=lambda mp: mp['progress'].get('progressPercent') if 'progress' in mp else None,
                new_name='grade_percent'),
    BaseMapping(get_lambda=lambda mp: mp['progress'].get('progressScore') if 'progress' in mp else None,
                new_name='grade_letter'),
    BaseMapping(get_lambda=lambda mp: mp['progress'].get('progressPointsEarned') if 'progress' in mp else None,
                new_name='points_earned'),
    BaseMapping(get_lambda=lambda mp: mp['progress'].get('progressTotalPoints') if 'progress' in mp else None,
                new_name='points_total'),
    NestedListMapping(mappings=assignment_mapping, old_name='assignments', new_name='assignments'),
]

grade_section_mapping = [
    BaseMapping(old_name='taskName', new_name='name'),
    BaseMapping(old_name='progressScore', new_name='grade_letter'),
    BaseMapping(old_name='progressPercent', new_name='grade_percent'),
    BaseMapping(old_name='categories', new_name='grade_sections'),
    NestedListMapping(mappings=grade_category_mapping, old_name='categories', new_name='grade_categories'),
]

course_mapping = [
    BaseMapping(old_name='sectionID', new_name='id', format_lambda=int),
    BaseMapping(old_name='courseName', new_name='name'),
    BaseMapping(old_name='teacherDisplay', new_name='teacher'),
    BaseMapping(get_lambda=lambda mp: get_grading_task_field(mp.get('gradingTasks'), 'percent', 'progressPercent'),
                new_name='grade_percent'),
    BaseMapping(get_lambda=lambda mp: get_grading_task_field(mp.get('gradingTasks'), 'score', 'progressScore'),
                new_name='grade_letter'),
    BaseMapping(old_name='teacherDisplay', new_name='teacher'),
    NestedListMapping(mappings=grade_section_mapping, old_name='details', new_name='grade_sections'),
]


@ns.route('/courses')
class CourseList(Resource):
    """
    For managing an overall list of the users courses.
    """
    @ns.marshal_list_with(course, skip_none=True)
    def get(self):
        """
        A list of the users classes with basic information.
        :return: A list of the users classes with basic information.
        """
        args = req_args.parse_args()
        app_url = urlparse(args['app_url'])

        response = requests.get(app_url.geturl() + '/resources/portal/grades', cookies={
            'JSESSIONID': args['JSESSIONID'],
            'appName': args['app_name'],
            'Domain': app_url.netloc,
            'campus_hybrid_app': 'student'
        })

        if response.status_code != 200:
            abort(response.status_code, 'Error occurred while accessing Infinite Campus.')

        if 'term' in args and args['term'] is not None:
            terms = [term for term in response.json()[0]['terms'] if term['termSeq'] == args['term']]
            if len(terms) == 0:
                abort(404, 'Term {} not found.'.format(args['term']))
            response = terms[0]['courses']
        else:
            response = response.json()[0]['courses']

        return apply_mapping(response, course_mapping), 200


@ns.route('/courses/<int:course_id>')
@ns.param('course_id', 'The course identifier.')
class Course(Resource):
    """
    For getting detailed information about a specific course.
    """
    @ns.marshal_with(course, skip_none=True)
    def get(self, course_id):
        """
        Information for a specific course.
        :return: Detailed information for the specified course.
        """
        args = req_args.parse_args()
        app_url = urlparse(args['app_url'])

        response = requests.get(app_url.geturl() + '/resources/portal/grades/detail/' + str(course_id), cookies={
            'JSESSIONID': args['JSESSIONID'],
            'appName': args['app_name'],
            'Domain': app_url.netloc,
            'campus_hybrid_app': 'student'
        })

        if response.status_code != 200:
            abort(response.status_code, 'Error occurred while accessing Infinite Campus.')

        return apply_mapping(response.json(), course_mapping), 200
