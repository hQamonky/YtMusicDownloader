# Import the framework
from flask_restful import Resource, reqparse
from src.endpoints import Controller


# Channels -------------------------------------------------------------------------------------------------------------


class Channels(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.get_channels()}, 200

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('channel', required=True)
        parser.add_argument('separator', required=True)
        parser.add_argument('artist_before_title', required=True)
        args = parser.parse_args()
        return {'message': 'Channel has been added.', 'data': Controller.new_channel(args)}, 201


class Channel(Resource):
    @staticmethod
    def get(identifier):
        return {'message': 'Success', 'data': Controller.get_channel(identifier)}, 200

    @staticmethod
    def post(identifier):
        parser = reqparse.RequestParser()
        parser.add_argument('separator', required=True)
        parser.add_argument('artist_before_title', required=True)
        args = parser.parse_args()
        return {'message': 'Channel has been updated.', 'data': Controller.update_channel(identifier, args)}, 201

    @staticmethod
    def delete(identifier):
        return {'message': 'Channel has been removed.', 'data': Controller.delete_channel(identifier)}, 200
