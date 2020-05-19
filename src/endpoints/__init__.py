import markdown
import os
import atexit

# Import the framework
from flask import Flask
from flask_restful import Resource, Api, reqparse
from src.controller import Controller
from apscheduler.schedulers.background import BackgroundScheduler

from src.endpoints.playlists import Playlists, Playlist, DownloadPlaylists, DownloadPlaylist
from src.endpoints.music import Music, NewMusic
from src.endpoints.naming_rules import NamingRules, NamingRule
from src.endpoints.channels import Channels, Channel

# Create an instance of Flask
app = Flask(__name__)
# Create the API
api = Api(app)

import src.endpoints.ui


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
