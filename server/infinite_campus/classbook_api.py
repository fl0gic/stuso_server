# Caden Kriese - 03-17-2020
from flask_restful import Resource
from flask import request


class ClassbooksAPI(Resource):
    @staticmethod
    def get():
        args = request.args
        jsessionid = args['jsessionid']
        app_name = args['app_name']

        # TODO send HTTP get request to /resources/portal/grades, parse & return results
