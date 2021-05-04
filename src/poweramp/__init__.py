from urllib.parse import unquote, urlparse
import os
from pathlib import Path


class PowerAmp:
    music_path = ""
    playlists_path = ""

    def __init__(self, music_path):
        self.music_path = music_path
        self.playlists_path = music_path + "/Playlists/PowerAmp"

    def convert_playlists_from_mopidy(self, mopidy_playlists_path):
        for filename in os.listdir(mopidy_playlists_path):
            f = os.path.join(mopidy_playlists_path, filename)
            # checking if it is a file
            if os.path.isfile(f):
                print("Treating file : " + f)
                # Check if it's a playlist file
                if filename.endswith('.m3u8'):
                    self.convert_playlist_from_mopidy(f)
                else:
                    print("File is not a playlist!")
            else:
                print("Not a file.")
        return

    def convert_playlist_from_mopidy(self, playlist):
        print("Converting " + playlist + "...")
        tmp_playlist_filename = playlist.split('/')
        print(tmp_playlist_filename)
        playlist_filename = tmp_playlist_filename[len(tmp_playlist_filename) - 1]
        self.create_playlist(playlist_filename.replace(".m3u8", ''))
        f = open(playlist, 'r')
        music_folder = self.music_path.split('/')[len(self.music_path.split('/')) - 1]
        for line in f:
            print("Converting line : " + line)
            new_playlist = open(self.playlists_path + "/" + playlist_filename, 'a')
            new_line = PowerAmp.convert_uri_to_path(line.replace("local:track:", "file:///"))
            print("new_line = " + new_line)
            new_playlist.write("#EXT-X-RATING:0\n"
                               "primary/" + music_folder + new_line.replace('', ''))
        return

    def create_playlist(self, name):
        playlist_full_path = self.playlists_path + "/" + name + ".m3u8"
        if self.check_if_playlist_exists(name):
            # Delete Playlist
            os.remove(playlist_full_path)
            print('Playlist existed -> was removed')
        # Create directories
        Path(self.playlists_path).mkdir(parents=True, exist_ok=True)
        # Create playlist file
        f = open(playlist_full_path, 'w')
        f.write("#EXTM3U\n")
        f.close()
        return "Playlist created!"

    def check_if_playlist_exists(self, playlist):
        return os.path.exists(self.playlists_path + "/" + playlist + ".m3u8")

    @staticmethod
    def convert_uri_to_path(uri):
        return unquote(urlparse(uri).path)
