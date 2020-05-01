# Caden Kriese - 04-10-2020
"""
Models for all API namespaces.
"""

from flask_restx import fields, Model

assignment = Model('assignment', {
    'name': fields.String(description='The name of the assignment.'),
    'date_assigned': fields.Date(description='The date the assignment was assigned.'),
    'date_due': fields.Date(description='The date the assignment was due.'),
    'points_earned': fields.Float(description='The amount of points earned on this assignment.'),
    'points_total': fields.Float(description='The total possible points of this assignment.'),
    'flags': fields.List(fields.String(enum=['late', 'missing', 'dropped', 'incomplete']))
})

grade_category = Model('grade_category', {
    'name': fields.String(description='The name of the grade category.'),
    'weight': fields.Float(description='The weight of the grade category.'),
    'excluded': fields.Float(description='The weight of the grade category.'),
    'grade_letter': fields.String(description='The letter grade of the grade category.'),
    'grade_percent': fields.Float(description='The percent grade of the grade category.'),
    'points_earned': fields.Float(description='The amount of points earned in this category.'),
    'points_total': fields.Float(description='The max amount of points in this category.'),
    'assignments': fields.List(fields.Nested(assignment, skip_none=True),
                               description='All assignments in this grade category.')
})

grade_section = Model('grade_section', {
    'name': fields.String(description='The name of the grade section.'),
    'grade_letter': fields.String(description='The letter grade of the grade section.'),
    'grade_percent': fields.Float(description='The percent grade of the grade section.'),
    'grade_categories': fields.List(fields.Nested(grade_category, skip_none=True),
                                    description='Grade categories in this section.')
})

course = Model('course', {
    'id': fields.Integer(description='The unique ID of the course.'),
    'name': fields.String(description='The name of the course.'),
    'teacher': fields.String(description='The name of the course.'),
    'grade_percent': fields.Float(description='The users current percentage grade in the course.'),
    'grade_letter': fields.String(description='The users current letter grade in the course.'),
    'grade_sections': fields.List(fields.Nested(grade_section, skip_none=True),
                                  description='Grade sections of this course.')
})
