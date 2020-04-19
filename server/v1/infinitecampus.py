# Caden Kriese - 03-17-2020
"""
API for Infinite Campus courses.
"""

from flask.views import MethodView
from flask_smorest import Blueprint

bp = Blueprint(
    'infinite_campus', 'Infinite Campus module.', url_prefix='/api/v1/ic',
    description='Infinite Campus module of the API.'
)


@bp.route('/courses')
class CourseList(MethodView):
    """
    API for listing basic information about all courses of a specific student.
    """
    def get(self):
        """
        Gets a list of all courses.
        ---
        :return: All courses the student is currently enrolled in.
        """
        return {'message': ':)'}, 200
        # args = request.args
        # app_url = args['app_url']
        # app_name = args['app_name']
        # jsessionid = args['jsessionid']
        # app_domain = urlparse(app_url).netloc
        #
        # response = requests.get(app_url + 'resources/portal/grades/', cookies={
        #     'JSESSIONID': jsessionid,
        #     'appName': app_name,
        #     'Domain': app_domain
        # }).json()
        #
        # if 'term' in args:
        #     index = int(args['term'])
        #     courses = response[0]['terms'][index]['courses']
        # else:
        #     courses = response[0]['courses']
        #
        # # Filter out grading tasks with no detail
        # for course in courses:
        #     if 'gradingTasks' in course:
        #         course['gradingTasks'] = [task for task in course['gradingTasks']
        #                                   if 'hasDetail' in task and bool(task['hasDetail'])]
        #
        # formatted_courses = [{
        #     'name': course.get('courseName'),
        #     'teacher': course.get('teacherDisplay'),
        #     'letter_grade': get_grade_value(course, 'score'),
        #     'percent': get_grade_value(course, 'percent')
        # } for course in courses]
        #
        # return [remove_nulls(course) for course in formatted_courses], 200
