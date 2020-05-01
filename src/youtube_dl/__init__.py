import subprocess
import json


class YoutubeDl:
    @staticmethod
    def video_url():
        return "https://www.youtube.com/watch?v="

    @staticmethod
    def playlist_url():
        return "https://www.youtube.com/playlist?list="

    @staticmethod
    def get_version():
        return subprocess.run(["youtube-dl", "--version"], check=True, stdout=subprocess.PIPE,
                              universal_newlines=True)

    @staticmethod
    def update():
        process = subprocess.run(["youtube-dl", "--update"], check=True, stdout=subprocess.PIPE,
                                 universal_newlines=True)
        result = {"message": process.stdout[:-1], "update_type": "youtube-dl"}
        if process.stdout == "It looks like you installed youtube-dl with a package manager, pip, setup.py or a " \
                             "tarball. Please use that to update.\n":
            print("Using pip to update...")
            process = YoutubeDl.pip_upgrade()
            result = {"message": process.stdout[:-1], "update_type": "pip"}
        return result

    @staticmethod
    def pip_upgrade():
        return subprocess.run(["pip", "install", "youtube-dl", "--upgrade"], check=True, stdout=subprocess.PIPE,
                              universal_newlines=True)

    @staticmethod
    def list_playlist(url):
        process = subprocess.run(["youtube-dl", "-ci", "--flat-playlist", "-J", url],
                                 check=True, stdout=subprocess.PIPE, universal_newlines=True)
        json_string = '[' + process.stdout[:-1] + ']'
        js = json.loads(json_string)
        return js

    @staticmethod
    def get_video_info(url):
        process = subprocess.run(["youtube-dl", "-ci", "-J", url],
                                 check=True, stdout=subprocess.PIPE, universal_newlines=True)
        json_string = process.stdout[:-1]
        js = json.loads(json_string)
        return js

    @staticmethod
    def download_music(url, output):
        process = subprocess.run(["sudo", "youtube-dl", "-ci",
                                  "-x", "--audio-format", "mp3",
                                  "--write-thumbnail",
                                  "-o", output,
                                  url],
                                 check=True, stdout=subprocess.PIPE, universal_newlines=True)
        return process.stdout
