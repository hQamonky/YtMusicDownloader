from src.youtube_dl import YoutubeDl
from src.database import Database


class Controller:
    @staticmethod
    def create_database():
        Database.create()
        return "Database created"

    # Playlists --------------------------------------------------------------------------------------------------------

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
        print("yt_playlist : ")
        yt_playlist = YoutubeDl.list_playlist(YoutubeDl.playlist_url() + playlist_id)
        print(yt_playlist)
        # Get playlist info from database (not created yet)
        print("db_playlist : ")
        db_playlist = Database.get_playlist(playlist_id)
        print(db_playlist)
        # Get list of naming rules from database
        naming_rules = Database.get_naming_rules()
        # For each video in youtube playlist
        for video in yt_playlist['entries']:
            print('for video :')
            print(video)
            # if video is in playlist database
            if Database.is_new_music_in_playlist(playlist_id, video['id']):
                print('New music in this playlist...')
                # Get video info from youtube
                yt_video_info = YoutubeDl.get_video_info(YoutubeDl.video_url() + video['id'])
                # Download it
                YoutubeDl.download_music(YoutubeDl.video_url() + video['id'], "./" + video['id'] + ".webm")
                # Apply naming rules
                print(naming_rules)
                # for naming_rule in naming_rules:

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
                # Add entry to Playlist_Music table
            else:
                print('Music already downloaded -> skip')

        return playlist_id + " downloaded"

    # Naming Rules -----------------------------------------------------------------------------------------------------

    @staticmethod
    def get_naming_rules():
        return Database.get_naming_rules()

    @staticmethod
    def new_naming_rule(args):
        rule_id = Database.new_naming_rule(args.replace, args.replace_by, args.priority)
        return {
            "id": rule_id,
            "replace": args.replace,
            "replace_by": args.replace_by,
            "priority": args.priority
        }

    @staticmethod
    def get_naming_rule(identifier):
        return Database.get_naming_rule(identifier)

    @staticmethod
    def update_naming_rule(identifier, args):
        Database.update_naming_rule(identifier, args.replace, args.replace_by, args.priority)
        return {
            "id": identifier,
            "replace": args.replace,
            "replace_by": args.replace_by,
            "priority": args.priority
        }

    @staticmethod
    def delete_naming_rule(identifier):
        Database.delete_naming_rule(identifier)
        return "OK"

    # Channels -----------------------------------------------------------------------------------------------------

    @staticmethod
    def get_channels():
        return Database.get_channels()

    @staticmethod
    def new_channel(args):
        Database.new_channel(args.channel, args.separator, args.artist_before_title)
        return {
            "channel": args.channel,
            "separator": args.separator,
            "artist_before_title": args.artist_before_title
        }

    @staticmethod
    def get_channel(identifier):
        return Database.get_channel(identifier)

    @staticmethod
    def update_channel(identifier, args):
        Database.update_channel(identifier, args.separator, args.artist_before_title)
        return {
            "channel": args.channel,
            "separator": args.separator,
            "artist_before_title": args.artist_before_title
        }

    @staticmethod
    def delete_channel(identifier):
        Database.delete_channel(identifier)
        return "OK"

    # IN PROGRESS ------------------------------------------------------------------------------------------------------

    # Youtube-dl methods
    @staticmethod
    def get_video_info(video_id):
        result = YoutubeDl.get_video_info(YoutubeDl.video_url() + video_id)
        return result

    @staticmethod
    def download_music(video_id):
        result = YoutubeDl.download_music(YoutubeDl.video_url() + video_id, "./" + video_id + ".webm")
        return result
