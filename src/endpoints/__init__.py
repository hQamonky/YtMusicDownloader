import markdown
import os
import shelve

# Import the framework
from flask import Flask, g
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

        return {'message': 'Playlist has been updated', 'data': Controller.update_playlist(identifier, args)}, 201

    @staticmethod
    def delete(identifier):
        return {'message': 'Playlist has been removed', 'data': Controller.delete_playlist(identifier)}, 200


# class UpdateYoutubeDl(Resource):
#     @staticmethod
#     def get():
#         return {'message': 'Success', 'data': Controller.update_youtube_dl()}, 200
#
#
# class TestingYoutubeDl(Resource):
#     @staticmethod
#     def get():
#         return {'message': 'Success', 'data': Controller.list_playlist("PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT")}, 200


api.add_resource(Init, '/initiate')
api.add_resource(Playlists, '/playlists')
api.add_resource(Playlist, '/playlist/<identifier>')
# api.add_resource(UpdateYoutubeDl, '/update-youtube-dl')
# api.add_resource(TestingYoutubeDl, '/testing')
