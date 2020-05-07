import markdown
import os
import shelve

# Import the framework
from flask import Flask, g, json
from flask_restful import Resource, Api, reqparse
from src.controller import Controller

# Create an instance of Flask
app = Flask(__name__)
# Create the API
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("ytdl.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Route shows the README file.
@app.route('/')
def index():
    # Open README file
    # return "Hello world !"
    with open(os.path.dirname(app.root_path) + "/../docs/Api User Guide.md", 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()
        # Convert to HTML
        return markdown.markdown(content)


class Init(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.create_database()}, 200


class Config(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.get_configuration()}, 200


class ConfigUser(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('user', required=True)
        args = parser.parse_args()
        return {'message': 'Success', 'data': Controller.update_config_user(args)}, 200


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
        return {'message': 'Naming rule has been updated.', 'data': Controller.update_naming_rule(identifier, args)}, 201

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
api.add_resource(Init, '/initiate')
# Playlists
api.add_resource(Playlists, '/playlists')
api.add_resource(Playlist, '/playlist/<identifier>')
api.add_resource(DownloadPlaylist, '/playlist/<playlist_id>/download')
# Naming Rules
api.add_resource(NamingRules, '/naming-rules')
api.add_resource(NamingRule, '/naming-rule/<identifier>')
# Channels
api.add_resource(Channels, '/channels')
api.add_resource(Channel, '/channel/<identifier>')
