# Caden Kriese - 03-17-2020
"""
Infinite Campus module of Student Solutions backend API.
"""
from server.v1 import api
from server.v1.infinite_campus.courses import Course, CourseList

infinite_campus = api.namespace('infinitecampus',
                                description='API requests for grabbing data specifically from Infinite Campus.')
infinite_campus.add_resource(CourseList, '/courses')
infinite_campus.add_resource(Course, '/courses/<int:course_id>')
