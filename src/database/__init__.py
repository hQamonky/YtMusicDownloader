import sqlite3

database = 'ytMusicDownloader.db'


class Database:
    # Creates the database. Warning : this will override the existing database.
    @staticmethod
    def create():
        conn = sqlite3.connect(database)
        c = conn.cursor()
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
        data = c.execute(request)
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
        return playlist

    @staticmethod
    def get_playlist_music(id_playlist):
        music = Database.get(PlaylistMusic.select_playlist(id_playlist))
        return music

    @staticmethod
    def new_music(id_playlist, id_music, name, title, artist, channel, upload_date):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute(Music.insert(id_music, name, title, artist, channel, upload_date))
        c.execute(PlaylistMusic.insert(id_playlist, id_music))
        conn.commit()
        conn.close()
        return "Music added"


class Playlists:
    @staticmethod
    def create():
        return "CREATE TABLE Playlists (id text, name text, uploader text, folder text)"

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
               "(id text, name text, title text, artist text, channel text, upload_date date, new integer)"

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
        return "CREATE TABLE Playlist_Music (id integer, id_playlist text, id_music text)"

    @staticmethod
    def select_playlist(id_playlist):
        return "SELECT * FROM PlaylistMusic WHERE new = '" + id_playlist + "'"

    @staticmethod
    def select_music(id_music):
        return "SELECT * FROM PlaylistMusic WHERE id_music = '" + id_music + "'"

    @staticmethod
    def insert(id_playlist, id_music):
        return "INSERT INTO PlaylistMusic VALUES ('" \
               + id_playlist + "','" \
               + id_music + "')"

    @staticmethod
    def delete_playlist(id_playlist):
        return "DELETE FROM PlaylistMusic WHERE id_playlist = '" + id_playlist + "'"


class Channels:
    @staticmethod
    def create():
        return "CREATE TABLE Channels (channel text, separator text, artist_before_title integer)"

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
                 "id = '" + channel + "'"


class DownloadOccurrences:
    @staticmethod
    def create():
        return "CREATE TABLE DownloadOccurrences (occurrence text)"

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
        return "CREATE TABLE NamingRules (id integer, replace text, replace_by text, priority integer)"

    @staticmethod
    def select_all():
        return "SELECT * FROM NamingRules ORDER BY priority"

    @staticmethod
    def insert(replace, replace_by, priority):
        return "INSERT INTO NamingRules VALUES ('" \
               + replace + "','" \
               + replace_by + "','" \
               + priority + "')"

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
