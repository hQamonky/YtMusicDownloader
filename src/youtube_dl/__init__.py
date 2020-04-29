import subprocess
import json


class YoutubeDl:
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
    def list_playlist(link):
        process = subprocess.run(["youtube-dl", "-ciw", "--flat-playlist", "-J", link],
                                 check=True, stdout=subprocess.PIPE, universal_newlines=True)
        json_string = '[' + process.stdout[:-1] + ']'
        js = json.loads(json_string)
        return js
