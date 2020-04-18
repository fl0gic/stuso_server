# Caden Kriese - 03-17-2020
"""
API for Infinite Campus courses.
"""
from urllib.parse import urlparse

import requests
from flask_restx import Namespace, Resource, reqparse

from server.utils.response_filter import apply_mapping
from server.v1.models import *

ns = Namespace('infinitecampus', path='/ic',
               description='API requests for grabbing data specifically from Infinite Campus.')

ic_cookies = reqparse.RequestParser()
ic_cookies.add_argument('JSESSIONID', type=str, help='The users session ID with Infinite Campus.', location='cookies')
ic_cookies.add_argument('app_url', type=str, help='The URL of the Infinite Campus application.', location='cookies')
ic_cookies.add_argument('app_name', type=str, help='The name of the Infinite Campus application.', location='cookies')

# TODO potentially add basic grade info?
course_mapping = {
    'id': tuple(['sectionID', int]),
    'name': tuple(['courseName', str]),
    'teacher': tuple(['teacherDisplay', str]),
}


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
        cookies = ic_cookies.parse_args()
        app_url = urlparse(cookies['app_url'])

        response = requests.get(app_url.geturl() + '/resources/portal/grades/', cookies={
            'JSESSIONID': cookies['JSESSIONID'],
            'appName': cookies['app_name'],
            'Domain': app_url.netloc,
            'campus_hybrid_app': 'student'
        }).json()[0]['courses']

        return apply_mapping(response, course_mapping), 200

# class CourseList(Resource):
#     """
#     API for listing basic information about all courses of a specific student.
#     """
#
#     @staticmethod
#     def get():
#         """
#         Gets a list of all courses.
#         :return: All courses the student is currently enrolled in.
#         """
#         args = request.args
#         cookies = request.cookies
#         app_url = urlparse(cookies['app_url'])
#
#         response = requests.get(app_url.geturl() + 'resources/portal/grades/', cookies={
#             'JSESSIONID': cookies['jsessionid'],
#             'appName': cookies['app_name'],
#             'Domain': app_url.netloc,
#             'campus_hybrid_app': 'student'
#         }).json()
#
#         if 'AuthenticationException' in str(response):
#             return {'error': 'Invalid Session Token'}, 401
#
#         if 'term' in args:
#             index = int(args['term'])
#             courses = response[0]['terms'][index]['courses']
#         else:
#             courses = response[0]['courses']
#
#         # Filter out grading tasks with no detail
#         for course in courses:
#             if 'gradingTasks' in course:
#                 course['gradingTasks'] = [task for task in course['gradingTasks']
#                                           if 'hasDetail' in task and bool(task['hasDetail'])]
#
#         formatted_courses = [{
#             'name': course.get('courseName'),
#             'teacher': course.get('teacherDisplay'),
#             'course_id': course.get('sectionID'),
#             'letter_grade': get_grade_value(course, 'score'),
#             'percent': get_grade_value(course, 'percent')
#         } for course in courses]
#
#         return [remove_nulls(course) for course in formatted_courses], 200
#
#
# class Course(Resource):
#     """
#     API for listing detailed information about a specific course.
#     """
#
#     @staticmethod
#     def get(course_id):
#         """
#         Gets detailed information from the requested course.
#         :return: All courses the student is currently enrolled in.
#         """
#         cookies = request.cookies
#         app_url = urlparse(cookies['app_url'])
#
#         grade_response = requests.get(app_url.geturl() + 'resources/portal/grades/detail/' + course_id, cookies={
#             'JSESSIONID': cookies['jsessionid'],
#             'appName': cookies['app_name'],
#             'Domain': app_url.netloc,
#             'campus_hybrid_app': 'student'
#         }).json()
#
#         course_response = requests.get(cookies['app_url'] + 'resources/portal/section/' + course_id, params={
#             '_expand': 'terms'
#         }, cookies={
#             'JSESSIONID': cookies['jsessionid'],
#             'appName': cookies['app_name'],
#             'Domain': app_url.netloc,
#             'campus_hybrid_app': 'student',
#         }).json()
#
#         if 'AuthenticationException' in str(grade_response) or 'AuthenticationException' in str(course_response):
#             return {'error': 'Invalid Session Token'}, 401
#
#         detail = [detail for detail in grade_response['details'] if detail['task'].get('hasDetail')][0]
#         task = detail['task']
#         categories = detail['categories']
#
#         formatted_courses = {
#             'teacher': course_response.get('teacherDisplay'),
#             'name': course_response.get('courseName'),
#             'number': course_response.get('courseNumber'),
#             'task': {
#                 'name': task.get('taskName'),
#                 'letter_grade': task.get('score') if 'score' in task else task.get('progressScore'),
#                 'percentage_grade': task.get('percent') if 'percent' in task else task.get('progressPercent'),
#                 'categories': [{
#                     'name': category.get('name'),
#                     'weight': category.get('weight') if 'isWeighted' in category and category['isWeighted'] else None,
#                     'excluded': category['isExcluded'] if 'isExcluded' in category and category['isExcluded'] else None,
#                     'assignments': [{
#                         'name': assignment.get('assignmentName'),
#                         'date_due': assignment.get('dueDate'),
#                         'date_assigned': assignment.get('assignedDate'),
#                         'earned_points': float(assignment['score']) if 'score' in assignment and assignment[
#                             'score'] is not None else None,
#                         'total_points': float(assignment['totalPoints']) if 'totalPoints' in assignment and assignment[
#                             'totalPoints'] is not None else None,
#                         'flags': [
#                             'late' if assignment.get('late') else None,
#                             'missing' if assignment.get('missing') else None,
#                             'cheated' if assignment.get('cheated') else None,
#                             'dropped' if assignment.get('dropped') else None,
#                             'incomplete' if assignment.get('incomplete') else None
#                         ]
#                     } for assignment in category['assignments']]
#                 } for category in categories]
#             }
#         }
#
#         return remove_nulls(formatted_courses), 200
