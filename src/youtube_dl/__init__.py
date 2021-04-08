import subprocess
import json
import requests


class YoutubeDl:

    path = ""

    def __init__(self, path):
        self.path = path

    @staticmethod
    def video_url():
        return "https://www.youtube.com/watch?v="

    @staticmethod
    def playlist_url():
        return "https://www.youtube.com/playlist?list="

    @staticmethod
    def pwd():
        process = subprocess.run(["pwd"], check=True, stdout=subprocess.PIPE,
                                 universal_newlines=True)
        return process.stdout[:-1]

    def get_version(self):
        process = subprocess.run([self.path, "--version"], check=True, stdout=subprocess.PIPE,
                                 universal_newlines=True)
        return process.stdout[:-1]

    def update(self):
        process = subprocess.run([self.path, "--update"], check=True, stdout=subprocess.PIPE,
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

    def list_playlist(self, url):
        print('running command : ' + self.path + " -ci --flat-playlist -J " + url)
        process = subprocess.run([self.path, "-ci",
                                  # "--min-sleep-interval", "4",
                                  # "--max-sleep-interval", "10",
                                  "--flat-playlist", "-J", url],
                                 check=True, stdout=subprocess.PIPE, universal_newlines=True)
        json_string = process.stdout[:-1]
        js = json.loads(json_string)
        return js

    def get_video_info(self, url):
        process = subprocess.run([self.path, "-ci",
                                  # "--min-sleep-interval", "4",
                                  # "--max-sleep-interval", "10",
                                  # "--cookies", "./src/youtube_dl/cookies.txt",
                                  "-J", url],
                                 check=True, stdout=subprocess.PIPE, universal_newlines=True)
        json_string = process.stdout[:-1]
        js = json.loads(json_string)
        return js

    @staticmethod
    def get_video_info_without_ytdl(url):
        full_url = "https://www.youtube.com/oembed?url=" + url + "&format=json"
        r = requests.get(url=full_url)
        data = r.json()
        print(data)
        return data

    def download_music(self, url, output):
        print('running command : ' + self.path + " -ci -x --audio-format mp3 --embed-thumbnail -o " + output + " "
              + url)
        process = subprocess.run([self.path, "-ci",
                                  "-x", "--audio-format", "mp3",
                                  "--embed-thumbnail",
                                  "-o", output,
                                  url],
                                 check=True, stdout=subprocess.PIPE, universal_newlines=True)
        return process.stdout
