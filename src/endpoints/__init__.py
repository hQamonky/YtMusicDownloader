import markdown
import os

# Import the framework
from flask import Flask
from flask_restful import Resource, Api, reqparse
from src.controller import Controller

# Create an instance of Flask
app = Flask(__name__)
# Create the API
api = Api(app)


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
    @staticmethod
    def get():
        return {'message': 'Success', 'data': 'null'}, 200


class UpdateYoutubeDl(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.update_youtube_dl()}, 200


class TestingYoutubeDl(Resource):
    @staticmethod
    def get():
        return {'message': 'Success', 'data': Controller.download_music("")}, 200


api.add_resource(Playlists, '/playlists')
api.add_resource(UpdateYoutubeDl, '/update-youtube-dl')
api.add_resource(TestingYoutubeDl, '/testing')
