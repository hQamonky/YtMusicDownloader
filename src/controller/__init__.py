import mutagen

from src.youtube_dl import YoutubeDl
from src.database import Database
import json
import os
import subprocess
from mutagen.easyid3 import EasyID3


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
                yt_video_info = YoutubeDl.get_video_info(YoutubeDl.video_url() + video['id'])
                # Download video
                YoutubeDl.download_music(YoutubeDl.video_url() + video['id'], "./" + video['id'] + ".webm")
                # Get channel info from database
                channel = Database.get_channel(yt_video_info['uploader'])
                # if channel not found
                if channel == yt_video_info['uploader']:
                    # Get default naming format from configuration file
                    with open('./configuration.json') as json_file:
                        config = json.load(json_file)
                        naming_format = config['naming_format']
                        separator = naming_format['separator']
                        artist_before_title = naming_format['artist_before_title']
                    # Insert channel entry in database with default naming format
                    Database.new_channel(channel, separator, artist_before_title)
                    channel = {'channel': channel, 'separator': separator, 'artist_before_title': artist_before_title}
                print('Channel : ' + channel['channel'])
                # Set title and artist
                title = yt_video_info['alt_title']
                artist = yt_video_info['creator']
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
                year = yt_video_info['upload_date'][:-4]
                print('Year : ' + year)
                # Set comment
                comment = '{\"platform\": \"youtube\", \"id\": \"' + video['id'] + '\"}'
                print('Comment : ' + comment)
                # Set permissions to downloaded file
                file = r'./' + video['id'] + '.mp3'
                subprocess.run(["sudo", "chmod", "o+rw", file],
                               check=True, stdout=subprocess.PIPE, universal_newlines=True)
                # Set metadata tags
                Controller.set_id3_tags(file, title, artist, album, year, comment)
                # Rename and move file to output playlist folder
                output_folder = r'' + db_playlist['folder']
                os.makedirs(output_folder, exist_ok=True)
                os.rename(file, output_folder + '/' + yt_video_info['title'] + '.mp3')
                # Insert Music in database
                # Add entry to Playlist_Music table
                log['downloaded'].append({
                    'id': video['id'],
                    'name': yt_video_info['title'],
                    'title': title,
                    'artist': artist,
                    'channel': album,
                    'upload_date': year,
                    'new': '1'
                })
            else:
                print('Music already downloaded -> skip')
                log['skipped'].append(video['id'])

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
            "channel": args.channel,
            "separator": args.separator,
            "artist_before_title": args.artist_before_title
        }

    @staticmethod
    def delete_channel(identifier):
        Database.delete_channel(identifier)
        return "OK"

    # Other ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def set_id3_tags(file, title, artist, album, year, comment):
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
        if year:
            tag['date'] = year
        if comment:
            EasyID3.RegisterTextKey("comment", "COMM")
            tag['comment'] = comment
        tag.save(v2_version=3)

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
