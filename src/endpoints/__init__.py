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


class Playlists(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])

        return {'message': 'Success', 'data': devices}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('device_type', required=True)
        parser.add_argument('controller_gateway', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identifier']] = args

        return {'message': 'Device registered', 'data': args}, 201


class UpdateYoutubeDl(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.update_youtube_dl()}, 200


class TestingYoutubeDl(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.list_playlist("PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT")}, 200


api.add_resource(Playlists, '/playlists')
api.add_resource(UpdateYoutubeDl, '/update-youtube-dl')
api.add_resource(TestingYoutubeDl, '/testing')
