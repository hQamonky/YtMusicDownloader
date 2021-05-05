# Import the framework
from flask_restful import Resource, reqparse
from src.endpoints import Controller

# Playlists ------------------------------------------------------------------------------------------------------------


class Playlists(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.get_playlists()}, 200

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True)
        parser.add_argument('name', required=True)
        # Parse the arguments into an object
        args = parser.parse_args()

        return {'message': 'Playlist has been added', 'data': Controller.new_playlist(args)}, 201


class ConvertPlaylists(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.convert_mopidy_playlists_to_power_amp()}, 200


class DownloadPlaylists(Resource):
    @staticmethod
    def post():
        return {'message': 'Success', 'data': Controller.download_playlists()}, 201


class Playlist(Resource):
    @staticmethod
    def get(identifier):
        return {'message': 'Success', 'data': Controller.get_playlist(identifier)}, 200

    @staticmethod
    def post(identifier):
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True)
        parser.add_argument('name', required=True)
        # Parse the arguments into an object
        args = parser.parse_args()

        return {'message': 'Playlist has been updated.', 'data': Controller.update_playlist(identifier, args)}, 201

    @staticmethod
    def delete(identifier):
        return {'message': 'Playlist has been removed.', 'data': Controller.delete_playlist(identifier)}, 200


class DownloadPlaylist(Resource):
    @staticmethod
    def post(playlist_id):
        return {'message': 'Success', 'data': Controller.download_playlist(playlist_id)}, 201


