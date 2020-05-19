# Import the framework
from flask_restful import Resource, reqparse
from src.endpoints import Controller


# Naming Rules ---------------------------------------------------------------------------------------------------------


class NamingRules(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.get_naming_rules()}, 200

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('replace', required=True)
        parser.add_argument('replace_by', required=True)
        parser.add_argument('priority', required=True)
        args = parser.parse_args()
        return {'message': 'Naming rule has been added.', 'data': Controller.new_naming_rule(args)}, 201


class NamingRule(Resource):
    @staticmethod
    def get(identifier):
        return {'message': 'Success', 'data': Controller.get_naming_rule(identifier)}, 200

    @staticmethod
    def post(identifier):
        parser = reqparse.RequestParser()
        parser.add_argument('replace', required=True)
        parser.add_argument('replace_by', required=True)
        parser.add_argument('priority', required=True)
        args = parser.parse_args()
        return {'message': 'Naming rule has been updated.',
                'data': Controller.update_naming_rule(identifier, args)}, 201

    @staticmethod
    def delete(identifier):
        return {'message': 'Naming rule has been removed.', 'data': Controller.delete_naming_rule(identifier)}, 200
