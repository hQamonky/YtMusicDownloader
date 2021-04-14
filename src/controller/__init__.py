import mutagen

from src.mopidy import Mopidy
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
    def set_youtube_dl_path(path):
        # Get configuration file
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        config['youtube_dl_path'] = path
        with open('./src/configuration.json', 'w') as outfile:
            json.dump(config, outfile)
        return config

    @staticmethod
    def get_youtube_dl_path():
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        return config['youtube_dl_path']

    @staticmethod
    def set_download_path(path):
        if path[-1:] == '/':
            path = path[:-1]
        # Get configuration file
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        config['download_path'] = path
        with open('./src/configuration.json', 'w') as outfile:
            json.dump(config, outfile)
        return config

    @staticmethod
    def get_download_path():
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        return config['download_path']

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
    def set_mopidy_local_path(path):
        if path[-1:] == '/':
            path = path[:-1]
        # Get configuration file
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        config['mopidy_local_path'] = path
        with open('./src/configuration.json', 'w') as outfile:
            json.dump(config, outfile)
        return config

    @staticmethod
    def get_mopidy_local_path():
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        return config['mopidy_local_path']

    @staticmethod
    def set_mopidy_playlists_path(path):
        if path[-1:] == '/':
            path = path[:-1]
        # Get configuration file
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        config['mopidy_playlists_path'] = path
        with open('./src/configuration.json', 'w') as outfile:
            json.dump(config, outfile)
        return config

    @staticmethod
    def get_mopidy_playlists_path():
        with open('./src/configuration.json') as json_file:
            config = json.load(json_file)
        return config['mopidy_playlists_path']

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

    @staticmethod
    def update_youtube_dl():
        youtube_dl = YoutubeDl(Controller.get_youtube_dl_path())
        return youtube_dl.update()

    # Database ---------------------------------------------------------------------------------------------------------

    @staticmethod
    def clear_database():
        Database.create()
        return "Database created"

    @staticmethod
    def factory_reset():
        config = {
            "version": "2.3",
            "youtube_dl_path": "./src/youtube_dl/youtube-dl",
            "download_path": "/mnt/seagate6t/n_u/Music",
            "download_interval": "1",
            "mopidy_local_path": "/mnt/seagate6t/n_u/Music",
            "mopidy_playlists_path": "/home/pi/.local/share/mopidy/m3u",
            "use_custom_user": "false",
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
        youtube_dl = YoutubeDl(Controller.get_youtube_dl_path())
        yt_playlist = youtube_dl.list_playlist(args.url)
        print(yt_playlist)
        Database.new_playlist(yt_playlist['id'], args.name, yt_playlist['uploader'])
        mopidy = Mopidy(Controller.get_mopidy_local_path, Controller.get_mopidy_playlists_path())
        mopidy.create_playlist(args.name)
        return {
            "id": yt_playlist['id'],
            "your_playlist_name": args.name,
            "yt_playlist_name": yt_playlist['title'],
            "uploader": yt_playlist['uploader']
        }

    @staticmethod
    def get_playlist(identifier):
        return Database.get_playlist(identifier)

    @staticmethod
    def update_playlist(identifier, args):
        youtube_dl = YoutubeDl(Controller.get_youtube_dl_path())
        yt_playlist = youtube_dl.list_playlist(args.url)
        print(yt_playlist)
        Database.update_playlist(identifier, yt_playlist['id'], args.name, yt_playlist['uploader'])
        return {
            "id": identifier,
            "youtube_id": yt_playlist['id'],
            "name": args.name,
            "uploader": yt_playlist['uploader']
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
        # Get playlist info from database (not created yet)
        print("db_playlist : ")
        db_playlist = Database.get_playlist(playlist_id)
        print(db_playlist)
        # Get playlists youtube id
        youtube_id = db_playlist['youtube_id']
        # Update youtube-dl
        youtube_dl = YoutubeDl(Controller.get_youtube_dl_path())
        print(youtube_dl.get_version())
        # print('Checking for youtube-dl updates...')
        # print(youtube_dl.update()['message'])
        # Get playlist info from youtube
        print("yt_playlist : ")
        yt_playlist = youtube_dl.list_playlist(YoutubeDl.playlist_url() + youtube_id)
        print(yt_playlist)
        log = {
            'id': playlist_id,
            'youtube_id': db_playlist['youtube_id'],
            'name': db_playlist['name'],
            'uploader': db_playlist['uploader'],
            'skipped': [],
            'downloaded': []
        }
        # Get list of naming rules from database
        naming_rules = Database.get_naming_rules()
        # For each video in youtube playlist
        for video in yt_playlist['entries']:
            # remove "/" characters
            video_title = video['title'].replace("/", "")
            print('For video : ' + video_title + ' - ' + video['id'])
            # if video is not already in database
            if Database.is_new_music(video['id']):
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
                name = video_title
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
                output_folder = r'' + Controller.get_download_path()
                os.makedirs(output_folder, exist_ok=True)
                use_custom_user = Controller.get_use_custom_user()
                if use_custom_user == "true":
                    subprocess.run(["chown", "qmk", output_folder],
                                   check=True, stdout=subprocess.PIPE, universal_newlines=True)
                else:
                    subprocess.run(["chmod", "755", output_folder],
                                   check=True, stdout=subprocess.PIPE, universal_newlines=True)
                # Download video
                youtube_dl.download_music(YoutubeDl.video_url() + video['id'], output_folder + '/'
                                          + video_title + ".webm")
                # Set permissions to downloaded file
                file = output_folder + '/' + video_title + '.mp3'
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
                # Database.new_music(playlist_id, video['id'], video_title +'.mp3', title, artist, channel['channel'],
                #                    yt_video_info['upload_date'])
                Database.new_music(video['id'], video_title + '.mp3', title, artist, channel['channel'])
                # Add entry to Playlist_Music table
                log['downloaded'].append({
                    'id': video['id'],
                    'name': video_title,
                    'title': title,
                    'artist': artist,
                    'channel': album,
                    # 'upload_date': year,
                    'new': '1'
                })
            else:
                print('Music already downloaded -> skip')
                log['skipped'].append(video['id'])
            # if video is not in playlist database
            if Database.is_new_music_in_playlist(playlist_id, video['id']):
                print('Music is new in this playlist')
                Database.add_music_in_playlist(video['id'], playlist_id)
                # Add Music in Mopidy playlist
                mopidy = Mopidy(Controller.get_mopidy_local_path, Controller.get_mopidy_playlists_path())
                music = Database.get_music(video['id'])
                mopidy.add_music_to_playlist(music['name'], db_playlist['name'])
        # Clean sync conflicts
        Controller.clean_sync_conflicts("False")
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
        # --  Update metadata
        # Get file name
        music = Database.get_music(identifier)
        filename = music['name']
        # Get file locations
        path = Controller.get_download_path()
        # Apply tags
        Controller.update_id3_tags(path + '/' + filename, args.title, args.artist)

        return {
            "id": identifier,
            "title": args.title,
            "artist": args.artist,
            "new": args.new
        }

    @staticmethod
    def fix_old_music_tags():
        # Iterate on every music file
        directory = Controller.get_download_path()
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                print("Treating file : " + f)
                # Check that its an mp3 file
                if filename.endswith('.mp3'):
                    # Check tag values
                    tags = Controller.get_id3_tags(f)
                    title = ''
                    album = ''
                    if 'title' in tags:
                        title = tags['title'][0]
                        print("Initial title : ")
                        print(title)
                    else:
                        print('No title tag')
                    if 'album' in tags:
                        album = tags['album'][0]
                        print("Initial album : " + album)
                    else:
                        print('No album tag')
                    # if tag is incorrect
                    if title.endswith('"') and len(album) > 150:
                        # Fix title
                        title = title[:-1]
                        print("New title : " + title)
                        # Fix album
                        album = album.split('"')[0]
                        print("New album : " + album)
                        # Apply tags
                        Controller.fix_old_id3_tags(f, title, album)
                    else:
                        print("File is already ok.")
                else:
                    print('Not an mp3 file')
        return

    @staticmethod
    def clean_sync_conflicts(dry_run):
        log = {
            'Kept': [],
            'Deleted': []
        }
        # Iterate on every music file
        directory = Controller.get_download_path()
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                print("Treating file : " + f)
                # Check if it's a conflict file
                if ".sync-conflict-" in filename or filename.endswith('.webm') or filename.endswith('.webp'):
                    # Delete file
                    print("deleting file...")
                    if dry_run == "False":
                        os.remove(f)
                    log['Deleted'].append(f)
                else:
                    print("Keep file.")
                    log['Kept'].append(f)
        return log

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

    @staticmethod
    # def set_id3_tags(file, title, artist, album, year, comment):
    def update_id3_tags(file, title, artist):
        try:
            tag = EasyID3(file)
        except:
            tag = mutagen.File(file, easy=True)
            tag.add_tags()
        if title:
            tag['title'] = title
        if artist:
            tag['artist'] = artist
        tag.save(v2_version=3)

    @staticmethod
    def get_id3_tags(file):
        try:
            tag = EasyID3(file)
            return tag
        except:
            tag = mutagen.File(file, easy=True)
            tag.add_tags()
            return

    @staticmethod
    # def set_id3_tags(file, title, artist, album, year, comment):
    def fix_old_id3_tags(file, title, album):
        try:
            tag = EasyID3(file)
        except:
            tag = mutagen.File(file, easy=True)
            tag.add_tags()
        if title:
            tag['title'] = title
        if album:
            tag['album'] = album
        tag.save(v2_version=3)
