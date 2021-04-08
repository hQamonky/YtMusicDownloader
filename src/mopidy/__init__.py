from os import path
import pathlib
from urllib.parse import unquote, urlparse


class Mopidy:
    playlists_path = ""

    def __init__(self, playlists_path):
        self.playlists_path = playlists_path

    def create_playlist(self, name):
        if self.check_if_playlist_exists(name):
            return "Playlist already exists."
        else:
            # Create playlist file
            open(self.playlists_path + "/" + name + ".m3u8", 'a').close()
            return "Playlist created!"

    def check_if_playlist_exists(self, playlist):
        return path.exists(self.playlists_path + "/" + playlist + ".m3u8")

    def add_music_to_playlist(self, music, playlist):
        music_uri = "local:track:" + self.convert_path_to_uri(music)
        with open(self.playlists_path + "/" + playlist + ".m3u8", "a") as playlist_file:
            playlist_file.write("\n" + music_uri)
        return

    def archive_music(self, music):
        return

    @staticmethod
    def convert_path_to_uri(file_path):
        return pathlib.Path(file_path).as_uri()

    @staticmethod
    def convert_uri_to_path(uri):
        return unquote(urlparse(uri).path)
