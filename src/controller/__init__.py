import mutagen

from src.youtube_dl import YoutubeDl
from src.database import Database
import json
import os
import subprocess
from mutagen.easyid3 import EasyID3


class Controller:

    # Configuration ----------------------------------------------------------------------------------------------------

    @staticmethod
    def get_configuration():
        # Get configuration file
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        return config

    @staticmethod
    def set_download_interval(time):
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        config['download_interval'] = time
        with open('./src/configuration.json', 'w') as outfile:
            json.dump(config, outfile)
        return config

    @staticmethod
    def get_download_interval():
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        return int(config['download_interval'])

    @staticmethod
    def update_config_naming_format(args):
        # Get configuration file
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        config['naming_format']['separator'] = args.separator
        config['naming_format']['artist_before_title'] = args.artist_before_title
        with open('./src/configuration.json', 'w') as outfile:
            json.dump(config, outfile)
        return config

    @staticmethod
    def update_config_user(use_custom_user):
        return Controller.set_use_custom_user(use_custom_user)

    @staticmethod
    def set_use_custom_user(use):
        # Get configuration file
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        config['use_custom_user'] = use
        with open('./src/configuration.json', 'w') as outfile:
            json.dump(config, outfile)
        return config

    @staticmethod
    def get_use_custom_user():
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        return config['use_custom_user']

    # Database ---------------------------------------------------------------------------------------------------------

    @staticmethod
    def clear_database():
        Database.create()
        return "Database created"

    @staticmethod
    def factory_reset():
        config = {
            "version": "1.0",
            "download_interval": "12",
            "use_custom_user": "true",
            "naming_format": {
                "separator": " - ",
                "artist_before_title": "true"
            }
        }
        with open('./src/configuration.json', 'w') as outfile:
            json.dump(config, outfile)
        Database.create()
        Database.add_factory_entries()
        return "Configuration and Database restored"

    # Playlists --------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_playlists():
        return Database.get_playlists()

    @staticmethod
    def new_playlist(args):
        if args.folder[-1:] == '/':
            args.folder = args.folder[:-1]
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
        if args.folder[-1:] == '/':
            args.folder = args.folder[:-1]
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
    def download_playlists():
        playlists = Database.get_playlists()
        logs = []
        for playlist in playlists:
            logs.append(Controller.download_playlist(playlist['id']))
        return logs

    # Don't be scared
    @staticmethod
    def download_playlist(playlist_id):
        # Update youtube-dl
        print('Checking for youtube-dl updates...')
        print(YoutubeDl.update()['message'])
        # Get playlist info from youtube
        print("yt_playlist : ")
        yt_playlist = YoutubeDl.list_playlist(YoutubeDl.playlist_url() + playlist_id)
        print(yt_playlist)
        # Get playlist info from database (not created yet)
        print("db_playlist : ")
        db_playlist = Database.get_playlist(playlist_id)
        print(db_playlist)
        log = {
            'id': playlist_id,
            'name': db_playlist['name'],
            'uploader': db_playlist['uploader'],
            'folder': db_playlist['folder'],
            'skipped': [],
            'downloaded': []
        }
        # Get list of naming rules from database
        naming_rules = Database.get_naming_rules()
        # For each video in youtube playlist
        for video in yt_playlist['entries']:
            name = video['title']
            print('For video : ' + name + ' - ' + video['id'])
            # if video is in playlist database
            if Database.is_new_music_in_playlist(playlist_id, video['id']):
                print('New music in this playlist...')
                # Get video info from youtube
                # yt_video_info = YoutubeDl.get_video_info(YoutubeDl.video_url() + video['id'])
                yt_video_info = YoutubeDl.get_video_info_without_ytdl(YoutubeDl.video_url() + video['id'])
                # Get channel info from database
                # channel = Database.get_channel(yt_video_info['uploader'])
                channel = Database.get_channel(yt_video_info['author_name'])
                # if channel not found
                # if channel == yt_video_info['uploader']:
                if channel == yt_video_info['author_name']:
                    # Get default naming format from configuration file
                    with open('./src/configuration.json') as json_file:
                        config = json.load(json_file)
                        naming_format = config['naming_format']
                        separator = naming_format['separator']
                        artist_before_title = naming_format['artist_before_title']
                    # Insert channel entry in database with default naming format
                    Database.new_channel(channel, separator, artist_before_title)
                    channel = {'channel': channel, 'separator': separator, 'artist_before_title': artist_before_title}
                print('Channel : ' + channel['channel'])
                # Set title and artist
                # title = yt_video_info['alt_title']
                # artist = yt_video_info['creator']
                title = None
                artist = None
                if title is None or artist is None:
                    # Apply naming rules
                    print('Applying naming rules...')
                    for naming_rule in naming_rules:
                        name = name.replace(naming_rule['replace'], naming_rule['replace_by'])
                    print('Finale name : ' + name)
                # Set title
                if title is None:
                    title = name
                    split_name = name.split(channel['separator'])
                    if len(split_name) == 2:
                        if channel['artist_before_title'] == 'true':
                            title = split_name[1]
                        else:
                            title = split_name[0]
                # Set artist
                if artist is None:
                    artist = channel['channel']
                    split_name = name.split(channel['separator'])
                    if len(split_name) == 2:
                        if channel['artist_before_title'] == 'true':
                            artist = split_name[0]
                        else:
                            artist = split_name[1]
                print('Title : ' + title)
                print('Artist : ' + artist)
                # Set album
                album = channel['channel']
                print('Album : ' + album)
                # Set year
                # year = yt_video_info['upload_date'][:-4]
                # print('Year : ' + year)
                # Set comment
                comment = '{\"platform\": \"youtube\", \"id\": \"' + video['id'] + '\"}'
                print('Comment : ' + comment)
                # Prepare output folder
                output_folder = r'' + db_playlist['folder']
                os.makedirs(output_folder, exist_ok=True)
                use_custom_user = Controller.get_use_custom_user()
                if use_custom_user == "true":
                    subprocess.run(["chown", "qmk", output_folder],
                                   check=True, stdout=subprocess.PIPE, universal_newlines=True)
                else:
                    subprocess.run(["chmod", "755", output_folder],
                                   check=True, stdout=subprocess.PIPE, universal_newlines=True)
                # Download video
                YoutubeDl.download_music(YoutubeDl.video_url() + video['id'],
                                         output_folder + '/' + yt_video_info['title'] + ".webm")
                # Set permissions to downloaded file
                file = output_folder + '/' + yt_video_info['title'] + '.mp3'
                if use_custom_user == "true":
                    subprocess.run(["chown", "qmk", file],
                                   check=True, stdout=subprocess.PIPE, universal_newlines=True)
                else:
                    subprocess.run(["chmod", "644", file],
                                   check=True, stdout=subprocess.PIPE, universal_newlines=True)
                # Set metadata tags
                # Controller.set_id3_tags(file, title, artist, album, year, comment)
                Controller.set_id3_tags(file, title, artist, album, comment)
                # Insert Music in database
                # Database.new_music(playlist_id, video['id'], video['title']+'.mp3', title, artist, channel['channel'],
                #                    yt_video_info['upload_date'])
                Database.new_music(playlist_id, video['id'], video['title'] + '.mp3', title, artist, channel['channel'])
                # Add entry to Playlist_Music table
                log['downloaded'].append({
                    'id': video['id'],
                    'name': yt_video_info['title'],
                    'title': title,
                    'artist': artist,
                    'channel': album,
                    # 'upload_date': year,
                    'new': '1'
                })
            else:
                print('Music already downloaded -> skip')
                log['skipped'].append(video['id'])

        return log

    # Music ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_music(identifier):
        return Database.get_music(identifier)

    @staticmethod
    def get_new_music():
        return Database.get_new_music()

    @staticmethod
    def update_music(identifier, args):
        Database.update_music(identifier, args.title, args.artist, args.new)
        return {
            "id": identifier,
            "title": args.title,
            "artist": args.artist,
            "new": args.new
        }

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
            "channel": identifier,
            "separator": args.separator,
            "artist_before_title": args.artist_before_title
        }

    @staticmethod
    def delete_channel(identifier):
        Database.delete_channel(identifier)
        return "OK"

    # Other ------------------------------------------------------------------------------------------------------------

    @staticmethod
    # def set_id3_tags(file, title, artist, album, year, comment):
    def set_id3_tags(file, title, artist, album, comment):
        try:
            tag = EasyID3(file)
        except:
            tag = mutagen.File(file, easy=True)
            tag.add_tags()
        if title:
            tag['title'] = title
        if artist:
            tag['artist'] = artist
        if album:
            tag['album'] = album
        # if year:
        #     tag['date'] = year
        if comment:
            EasyID3.RegisterTextKey("comment", "COMM")
            tag['comment'] = comment
        tag.save(v2_version=3)
