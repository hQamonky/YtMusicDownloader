from os import path
import os
import pathlib

from src.poweramp import PowerAmp


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

    def get_music_to_remove(self, remove_playlist_name):
        music_to_remove = []
        # Iterate on "remove playlist"
        f = open(self.playlists_path + "/" + remove_playlist_name + ".m3u8", 'r')
        for line in f:
            print("Converting line : " + line)
            if line.startswith("local:track:Archive%"):
                # Sip if music is already archived
                continue
            music_to_remove.append(PowerAmp.convert_uri_to_path(line.replace("local:track:", '')))
        return music_to_remove

    def archive_music(self, music, remove_playlist_name):
        # Iterate on playlist files
        for filename in os.listdir(self.playlists_path):
            f = os.path.join(self.playlists_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                print("Remove playlist name = " + remove_playlist_name)
                if not f.endswith(remove_playlist_name + ".m3u8"):
                    print("Treating file : " + f)
                    # Check if it's a playlist file
                    if filename.endswith('.m3u8'):
                        # Remove music from playlist
                        self.remove_music_from_playlist(music, f)
                    else:
                        print("File is not a playlist!")
                else:
                    print("Ignoring remove playlist")
            else:
                print("Not a file.")
        return

    @staticmethod
    def remove_music_from_playlist(music, playlist):
        print("music : " + music)
        formatted_music = Mopidy.convert_path_to_uri("/" + music).replace("file:///", "local:track:") + "\n"
        print("formatted music : " + formatted_music)
        print("file to open : " + playlist)
        with open(playlist, "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                if i != formatted_music:
                    f.write(i)
            f.truncate()
        return

    @staticmethod
    def convert_path_to_uri(file_path):
        return pathlib.Path(file_path).as_uri()
