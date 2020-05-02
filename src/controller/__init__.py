import json

from flask import jsonify
from src.youtube_dl import YoutubeDl
from src.database import Database


class Controller:
    @staticmethod
    def create_database():
        Database.create()
        return "Database created"

    @staticmethod
    def get_playlists():
        return Database.get_playlists()

    @staticmethod
    def new_playlist(args):
        yt_playlist = YoutubeDl.list_playlist(args.url)
        Database.new_playlist(yt_playlist['id'], yt_playlist['title'], yt_playlist['uploader'], args.folder)
        return {
            "id": yt_playlist['id'],
            "name": yt_playlist['title'],
            "uploader": yt_playlist['uploader'],
            "folder": args.folder
        }

    @staticmethod
    def get_playlist(identifier):
        return Database.get_playlist(identifier)

    @staticmethod
    def update_playlist(identifier, args):
        playlist = Database.get_playlist(identifier)
        Database.update_playlist(identifier, playlist['name'], playlist['uploader'], args.folder)
        return {
            "id": identifier,
            "name": playlist['name'],
            "uploader": playlist['uploader'],
            "folder": args.folder
        }

    @staticmethod
    def delete_playlist(identifier):
        Database.delete_playlist(identifier)
        return "OK"

    @staticmethod
    def download_playlist(playlist_id):
        # Update youtube-dl
        YoutubeDl.update()
        # Get playlist info from youtube
        yt_playlist = YoutubeDl.list_playlist(YoutubeDl.playlist_url() + playlist_id)
        # Get playlist info from database (not created yet)
        db_playlist = Database.get_playlist(playlist_id)
        db_music = Database.get_playlist_music(playlist_id)
        # for each video in youtube playlist :
        # if video is not in database :
        # Get video info from youtube
        # Download it
        # Get list of naming rules from database
        # Apply naming rules
        # Get channel info from database
        # if channel not found :
        # Get default naming format from configuration file
        # Insert channel entry in database with default naming format
        # end if
        # Set title, artist, thumbnail, date and comment to downloaded file
        # Delete downloaded thumbnail
        # Set permissions to downloaded file
        # Move file to output playlist folder
        # Insert Music in database
        # end if
        # end for

        return

    # Youtube-dl methods
    @staticmethod
    def get_video_info(video_id):
        result = YoutubeDl.get_video_info(YoutubeDl.video_url() + video_id)
        return result

    @staticmethod
    def download_music(video_id):
        result = YoutubeDl.download_music(YoutubeDl.video_url() + video_id, "./" + video_id + ".webm")
        return result
