from os import path
import pathlib


class Mopidy:
    local_path = ""
    playlists_path = ""

    def __init__(self, local_path, playlists_path):
        self.local_path = local_path
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
        print("Adding Music to Playlist")
        print("Music : " + music)
        print("Playlist : " + playlist)
        music_uri = self.convert_path_to_uri("/" + music)
        print("File URI : " + music_uri)
        mopidy_uri = music_uri.replace("file:///", "local:track:")
        print("Mopidy URI : " + mopidy_uri)
        with open(self.playlists_path + "/" + playlist + ".m3u8", "a") as playlist_file:
            playlist_file.write("\n" + mopidy_uri)
        return

    def archive_music(self, music):
        return

    @staticmethod
    def convert_path_to_uri(file_path):
        return pathlib.Path(file_path).as_uri()
