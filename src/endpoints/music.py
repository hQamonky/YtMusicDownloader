# Import the framework
from flask_restful import Resource, reqparse
from src.endpoints import Controller

# Music ----------------------------------------------------------------------------------------------------------------


class Music(Resource):
    @staticmethod
    def post(identifier):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('artist', required=True)
        parser.add_argument('new', required=True)
        args = parser.parse_args()
        return {'message': 'Music has been updated.', 'data': Controller.update_music(identifier, args)}, 201


class NewMusic(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.get_new_music()}, 200


class FixOldMusicTags(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.fix_old_music_tags()}, 200


class CleanSyncConflicts(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.clean_sync_conflicts("False")}, 200
