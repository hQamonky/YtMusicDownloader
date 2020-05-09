import markdown
import os
import atexit

# Import the framework
from flask import Flask
from flask_restful import Resource, Api, reqparse
from src.controller import Controller
from apscheduler.schedulers.background import BackgroundScheduler


def add_job_to_scheduler(interval):
    scheduler.add_job(func=Controller.download_playlists,
                      trigger="interval", hours=interval, id='download_playlists')


def start_scheduler(interval):
    if interval != -1:
        add_job_to_scheduler(interval)
        scheduler.start()


def restart_scheduler(interval):
    scheduler.remove_job('download_playlists')
    if interval != -1:
        add_job_to_scheduler(interval)


scheduler = BackgroundScheduler()
start_scheduler(Controller.get_download_interval())
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Create an instance of Flask
app = Flask(__name__)
# Create the API
api = Api(app)


# Route shows the user guide file.
@app.route('/')
def index():
    # Open file
    with open(os.path.dirname(app.root_path) + "/../docs/Api User Guide.md", 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()
        # Convert to HTML
        return markdown.markdown(content)


class AutoDownload(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('interval', required=True)
        args = parser.parse_args()
        result = Controller.set_download_interval(args.interval)
        # Restart job with updated interval
        restart_scheduler(int(args.interval))
        return {'message': 'Success', 'data': result}, 201


class FactoryReset(Resource):
    @staticmethod
    def post():
        return {'message': 'Success', 'data': Controller.factory_reset()}, 201


class Config(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.get_configuration()}, 200


class ConfigUser(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('use_custom_user', required=True)
        args = parser.parse_args()
        return {'message': 'Success', 'data': Controller.update_config_user(args.use_custom_user)}, 200


class ConfigNamingFormat(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('separator', required=True)
        parser.add_argument('artist_before_title', required=True)
        args = parser.parse_args()
        return {'message': 'Success', 'data': Controller.update_config_naming_format(args)}, 200


# Playlists ------------------------------------------------------------------------------------------------------------


class Playlists(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.get_playlists()}, 200

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True)
        parser.add_argument('folder', required=True)
        # Parse the arguments into an object
        args = parser.parse_args()

        return {'message': 'Playlist has been added', 'data': Controller.new_playlist(args)}, 201


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
        parser.add_argument('folder', required=True)
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


# INDEX ----------------------------------------------------------------------------------------------------------------
api.add_resource(Config, '/configuration')
api.add_resource(ConfigUser, '/configuration/user')
api.add_resource(ConfigNamingFormat, '/configuration/naming-format')
api.add_resource(FactoryReset, '/factory-reset')
api.add_resource(AutoDownload, '/auto-download')
# Playlists
api.add_resource(Playlists, '/playlists')
api.add_resource(DownloadPlaylists, '/playlists/download')
api.add_resource(Playlist, '/playlist/<identifier>')
api.add_resource(DownloadPlaylist, '/playlist/<playlist_id>/download')
# Music
api.add_resource(NewMusic, '/music/new')
api.add_resource(Music, '/music/<identifier>')
# Naming Rules
api.add_resource(NamingRules, '/naming-rules')
api.add_resource(NamingRule, '/naming-rule/<identifier>')
# Channels
api.add_resource(Channels, '/channels')
api.add_resource(Channel, '/channel/<identifier>')
