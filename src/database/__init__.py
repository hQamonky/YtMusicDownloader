import sqlite3

database = 'ytMusicDownloader.db'


class Database:
    # Creates the database. Warning : this will override the existing database.
    @staticmethod
    def create():
        conn = sqlite3.connect(database)
        c = conn.cursor()
        # Delete tables if exists
        c.execute(Playlists.drop())
        c.execute(Music.drop())
        c.execute(PlaylistMusic.drop())
        c.execute(DownloadOccurrences.drop())
        c.execute(NamingRules.drop())
        c.execute(Channels.drop())

        # Create tables
        c.execute(Playlists.create())
        c.execute(Music.create())
        c.execute(PlaylistMusic.create())
        c.execute(DownloadOccurrences.create())
        c.execute(NamingRules.create())
        c.execute(Channels.create())
        # Save (commit) the changes
        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    @staticmethod
    def edit(request):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        # Insert new entries
        c.execute(request)
        # Save (commit) the changes
        conn.commit()
        # Close the connection
        conn.close()

    @staticmethod
    def get(request):
        conn = sqlite3.connect(database)
        # Convert data format to json
        conn.row_factory = Database.dict_factory
        c = conn.cursor()
        # Insert new entries
        data = c.execute(request).fetchall()
        # Save (commit) the changes
        conn.commit()
        # Close the connection
        conn.close()
        return data

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # Playlists --------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_playlists():
        playlists = Database.get(Playlists.select_all())
        return playlists

    @staticmethod
    def new_playlist(identifier, name, uploader, folder):
        Database.edit(Playlists.insert(identifier, name, uploader, folder))
        return "Playlist added"

    @staticmethod
    def get_playlist(id_playlist):
        playlist = Database.get(Playlists.select(id_playlist))
        return playlist[0]

    @staticmethod
    def update_playlist(id_playlist, name, uploader, folder):
        Database.edit(Playlists.update(id_playlist, name, uploader, folder))
        return "Playlist updated"

    @staticmethod
    def delete_playlist(id_playlist):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        # Delete entry in Playlists table
        c.execute(Playlists.delete(id_playlist))
        # Delete all entries in Playlist_Music table with id_playlist
        c.execute(PlaylistMusic.delete_playlist(id_playlist))
        conn.commit()
        conn.close()
        return "Playlist removed"

    @staticmethod
    def is_new_music_in_playlist(id_playlist, id_music):
        count = Database.get(PlaylistMusic.count_playlist_music(id_playlist, id_music))[0]['COUNT(*)']
        if count == 0:
            return True
        else:
            return False

    # Naming Rules -----------------------------------------------------------------------------------------------------

    @staticmethod
    def get_naming_rules():
        rules = Database.get(NamingRules.select_all())
        return rules

    @staticmethod
    def new_naming_rule(replace, replace_by, priority):
        Database.edit(NamingRules.insert(replace, replace_by, priority))
        identifier = Database.get(NamingRules.get_id_of_last_entry())
        return identifier[0]['id']

    @staticmethod
    def get_naming_rule(id_rule):
        rule = Database.get(NamingRules.select(id_rule))
        return rule[0]

    @staticmethod
    def update_naming_rule(identifier, replace, replace_by, priority):
        Database.edit(NamingRules.update(identifier, replace, replace_by, priority))
        return "Naming Rule updated"

    @staticmethod
    def delete_naming_rule(identifier):
        Database.edit(NamingRules.delete(identifier))
        return "Naming Rule removed"

    # Channels ---------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_channels():
        rules = Database.get(Channels.select_all())
        return rules

    @staticmethod
    def new_channel(channel, separator, artist_before_title):
        Database.edit(Channels.insert(channel, separator, artist_before_title))
        return "Channel added"

    @staticmethod
    def get_channel(id_channel):
        channel = Database.get(Channels.select_channel(id_channel))
        if len(channel) == 0:
            return id_channel
        else:
            return channel[0]

    @staticmethod
    def update_channel(identifier, separator, artist_before_title):
        Database.edit(Channels.update(identifier, separator, artist_before_title))
        return "Channel updated"

    @staticmethod
    def delete_channel(identifier):
        Database.edit(Channels.delete(identifier))
        return "Channel removed"

    @staticmethod
    def new_music(id_playlist, id_music, name, title, artist, channel, upload_date):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute(Music.insert(id_music, name, title, artist, channel, upload_date))
        c.execute(PlaylistMusic.insert(id_playlist, id_music))
        conn.commit()
        conn.close()
        return "Music added"


# TODO : Protect requests from SQL injections

class Playlists:
    @staticmethod
    def create():
        return "CREATE TABLE Playlists (id text PRIMARY KEY, name text, uploader text, folder text)"

    @staticmethod
    def drop():
        return "DROP TABLE IF EXISTS Playlists"

    @staticmethod
    def select_all():
        return "SELECT * FROM Playlists"

    @staticmethod
    def select(identifier):
        return "SELECT * FROM Playlists WHERE id = '" + identifier + "'"

    @staticmethod
    def insert(identifier, name, uploader, folder):
        return "INSERT INTO Playlists VALUES ('" \
               + identifier + "','" \
               + name + "','" \
               + uploader + "','" \
               + folder + "')"

    @staticmethod
    def update(identifier, name, uploader, folder):
        return "UPDATE Playlists SET " \
               + "name = '" + name + "'," \
               + "uploader = '" + uploader + "'," \
               + "folder = '" + folder + "'" \
               + "WHERE " \
                 "id = '" + identifier + "'"

    @staticmethod
    def delete(identifier):
        return "DELETE FROM Playlists WHERE id = '" + identifier + "'"


class Music:
    @staticmethod
    def create():
        return "CREATE TABLE Music " \
               "(id text PRIMARY KEY, name text, title text, artist text, channel text, upload_date date, new integer)"

    @staticmethod
    def drop():
        return "DROP TABLE IF EXISTS Music"

    @staticmethod
    def select_new():
        return "SELECT * FROM Music WHERE new = '1'"

    @staticmethod
    def insert(identifier, name, title, artist, channel, upload_date):
        return "INSERT INTO Music VALUES ('" \
               + identifier + "','" \
               + name + "','" \
               + title + "','" \
               + artist + "','" \
               + channel + "','" \
               + upload_date + "','" \
               + "1')"

    @staticmethod
    def update(identifier, title, artist, new):
        return "UPDATE Music SET " \
               + "title = '" + title + "'," \
               + "artist = '" + artist + "'," \
               + "new = '" + new + "'" \
               + "WHERE " \
                 "id = '" + identifier + "'"

    @staticmethod
    def delete(identifier):
        return "DELETE FROM Music WHERE id = '" + identifier + "'"


class PlaylistMusic:
    @staticmethod
    def create():
        return "CREATE TABLE Playlist_Music (id INTEGER PRIMARY KEY AUTOINCREMENT, id_playlist text, id_music text)"

    @staticmethod
    def drop():
        return "DROP TABLE IF EXISTS Playlist_Music"

    @staticmethod
    def select_playlist(id_playlist):
        return "SELECT * FROM Playlist_Music WHERE id_playlist = '" + id_playlist + "'"

    @staticmethod
    def select_music(id_music):
        return "SELECT * FROM Playlist_Music WHERE id_music = '" + id_music + "'"

    @staticmethod
    def count_playlist_music(id_playlist, id_music):
        return "SELECT COUNT(*) FROM Playlist_Music " \
               "WHERE id_playlist = '" + id_playlist + "' AND id_music = '" + id_music + "'"

    @staticmethod
    def insert(id_playlist, id_music):
        return "INSERT INTO Playlist_Music (id_playlist, id_music) VALUES ('" \
               + id_playlist + "','" \
               + id_music + "')"

    @staticmethod
    def delete_playlist(id_playlist):
        return "DELETE FROM Playlist_Music WHERE id_playlist = '" + id_playlist + "'"


class Channels:
    @staticmethod
    def create():
        return "CREATE TABLE Channels (channel text PRIMARY KEY, separator text, artist_before_title integer)"

    @staticmethod
    def drop():
        return "DROP TABLE IF EXISTS Channels"

    @staticmethod
    def select_all():
        return "SELECT * FROM  Channels "

    @staticmethod
    def select_channel(channel):
        return "SELECT * FROM  Channels WHERE channel = '" + channel + "'"

    @staticmethod
    def insert(channel, separator, artist_before_title):
        return "INSERT INTO  Channels  VALUES ('" \
               + channel + "','" \
               + separator + "','" \
               + artist_before_title + "')"

    @staticmethod
    def update(channel, separator, artist_before_title):
        return "UPDATE  Channels  SET " \
               + "separator = '" + separator + "'," \
               + "artist_before_title = '" + artist_before_title + "'" \
               + "WHERE " \
                 "channel = '" + channel + "'"

    @staticmethod
    def delete(identifier):
        return "DELETE FROM Channels WHERE channel = '" + identifier + "'"


class DownloadOccurrences:
    @staticmethod
    def create():
        return "CREATE TABLE DownloadOccurrences (occurrence text PRIMARY KEY)"

    @staticmethod
    def drop():
        return "DROP TABLE IF EXISTS DownloadOccurrences"

    @staticmethod
    def select_all():
        return "SELECT * FROM DownloadOccurrences"

    @staticmethod
    def insert(time):
        return "INSERT INTO DownloadOccurrences VALUES ('" + time + "')"

    @staticmethod
    def delete(time):
        return "DELETE FROM DownloadOccurrences WHERE occurrence = '" + time + "'"


class NamingRules:
    @staticmethod
    def create():
        return "CREATE TABLE NamingRules " \
               "(id INTEGER PRIMARY KEY AUTOINCREMENT, replace text, replace_by text, priority integer)"

    @staticmethod
    def drop():
        return "DROP TABLE IF EXISTS NamingRules"

    @staticmethod
    def select_all():
        return "SELECT * FROM NamingRules ORDER BY priority"

    @staticmethod
    def select(identifier):
        return "SELECT * FROM NamingRules WHERE id = '" + identifier + "'"

    @staticmethod
    def insert(replace, replace_by, priority):
        return "INSERT INTO NamingRules (replace, replace_by, priority) VALUES ('" \
               + replace + "','" \
               + replace_by + "','" \
               + priority + "')"

    @staticmethod
    def get_id_of_last_entry():
        return "SELECT id FROM NamingRules ORDER BY id DESC LIMIT 1"

    @staticmethod
    def update(identifier, replace, replace_by, priority):
        return "UPDATE NamingRules SET " \
               + "replace = '" + replace + "'," \
               + "replace_by = '" + replace_by + "'," \
               + "priority = '" + priority + "'" \
               + "WHERE " \
                 "id = '" + identifier + "'"

    @staticmethod
    def delete(identifier):
        return "DELETE FROM NamingRules WHERE id = '" + identifier + "'"
