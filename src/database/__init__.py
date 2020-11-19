import sqlite3

database = './src/ytMusicDownloader.db'


class Database:
    @staticmethod
    def connect():
        conn = sqlite3.connect(database)
        # Convert data format to json
        conn.row_factory = Database.dict_factory
        return conn

    @staticmethod
    def close(conn):
        # Save (commit) the changes
        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # Creates the database. Warning : this will override the existing database.
    @staticmethod
    def create():
        connection = Database.connect()
        c = connection.cursor()

        # Delete tables if exists
        Playlists.drop(c)
        Music.drop(c)
        PlaylistMusic.drop(c)
        NamingRules.drop(c)
        Channels.drop(c)

        # Create tables
        Playlists.create(c)
        Music.create(c)
        PlaylistMusic.create(c)
        NamingRules.create(c)
        Channels.create(c)

        Database.close(connection)

    @staticmethod
    def add_factory_entries():
        connection = Database.connect()
        c = connection.cursor()

        # Add Pegboard Nerds channel
        Channels.insert(c, "Pegboard Nerds", " - ", "false")

        # Add naming rules
        # priority 1
        NamingRules.insert(c, " ‒ ", " - ", "1")
        # priority 2
        NamingRules.insert(c, " [NCS Release]", "", "2")
        NamingRules.insert(c, " [Monstercat Release]", "", "2")
        NamingRules.insert(c, " [Diversity Release]", "", "2")
        NamingRules.insert(c, " [NCS Official Video]", "", "2")
        NamingRules.insert(c, " [Monstercat FREE Release]", "", "2")
        NamingRules.insert(c, " [Monstercat Official Music Video]", "", "2")
        NamingRules.insert(c, " [Monstercat EP Release]", "", "2")
        NamingRules.insert(c, " [Tasty Release]", "", "2")
        NamingRules.insert(c, " | Diversity Release", "", "2")
        NamingRules.insert(c, " (Lyrics _ Lyric Video)", "", "2")
        NamingRules.insert(c, " | HQ Videoclip", "", "2")
        NamingRules.insert(c, " | Official Videoclip", "", "2")
        NamingRules.insert(c, " | Videoclip", "", "2")
        NamingRules.insert(c, " (Videoclip) ♦ Hardstyle ♦", "", "2")
        NamingRules.insert(c, " ♦ Hardstyle Remix (Videoclip) ♦", "", "2")
        NamingRules.insert(c, " [Videoclip]", "", "2")
        NamingRules.insert(c, " (Official Music Video)", "", "2")
        NamingRules.insert(c, " (Official Video Clip)", "", "2")
        NamingRules.insert(c, " (Official Videoclip)", "", "2")
        NamingRules.insert(c, " (Official Video)", "", "2")
        NamingRules.insert(c, " (Official Preview)", "", "2")
        NamingRules.insert(c, " (official music video)", "", "2")
        NamingRules.insert(c, " | Complexity Release", "", "2")
        NamingRules.insert(c, "[Audio]", "", "2")
        NamingRules.insert(c, "【𝙻𝚈𝚁𝙸𝙲𝚂】", "", "2")
        NamingRules.insert(c, "(Official Audio)", "", "2")
        NamingRules.insert(c, "	(Lyrics)", "", "2")
        # priority 3
        NamingRules.insert(c, "♦ Hardstyle ♦", "(Hardstyle)", "3")

        Database.close(connection)

    # Playlists --------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_playlists():
        connection = Database.connect()
        c = connection.cursor()
        playlists = Playlists.select_all(c)
        Database.close(connection)
        return playlists

    @staticmethod
    def new_playlist(identifier, name, uploader, folder):
        connection = Database.connect()
        c = connection.cursor()
        Playlists.insert(c, identifier, name, uploader, folder)
        Database.close(connection)
        return "Playlist added"

    @staticmethod
    def get_playlist(id_playlist):
        connection = Database.connect()
        c = connection.cursor()
        playlist = Playlists.select(c, id_playlist)
        Database.close(connection)
        return playlist[0]

    @staticmethod
    def update_playlist(id_playlist, name, uploader, folder):
        connection = Database.connect()
        c = connection.cursor()
        Playlists.update(c, id_playlist, name, uploader, folder)
        Database.close(connection)
        return "Playlist updated"

    @staticmethod
    def delete_playlist(id_playlist):
        connection = Database.connect()
        c = connection.cursor()
        # Delete entry in Playlists table
        Playlists.delete(c, id_playlist)
        # Delete all entries in Playlist_Music table with id_playlist
        PlaylistMusic.delete_playlist(c, id_playlist)
        Database.close(connection)
        return "Playlist removed"

    @staticmethod
    def is_new_music_in_playlist(id_playlist, id_music):
        connection = Database.connect()
        c = connection.cursor()
        count = PlaylistMusic.count_playlist_music(c, id_playlist, id_music)[0]['COUNT(*)']
        Database.close(connection)
        if count == 0:
            return True
        else:
            return False

    # Music ------------------------------------------------------------------------------------------------------------

    @staticmethod
    # def new_music(id_playlist, id_music, name, title, artist, channel, upload_date):
    def new_music(id_playlist, id_music, name, title, artist, channel):
        connection = Database.connect()
        c = connection.cursor()
        # Music.insert(c, id_music, name, title, artist, channel, upload_date)
        try:
            Music.insert(c, id_music, name, title, artist, channel)
        except sqlite3.IntegrityError:
            print("Error : Cannot insert Music in database. The entry might already exist ?")
        PlaylistMusic.insert(c, id_playlist, id_music)
        Database.close(connection)
        return "Music added"

    @staticmethod
    def update_music(id_music, title, artist, new):
        connection = Database.connect()
        c = connection.cursor()
        Music.update(c, id_music, title, artist, new)
        Database.close(connection)
        return "Music updated"

    @staticmethod
    def get_new_music():
        connection = Database.connect()
        c = connection.cursor()
        music = Music.select_new(c)
        Database.close(connection)
        return music

    @staticmethod
    def get_music(identifier):
        connection = Database.connect()
        c = connection.cursor()
        music = Music.select_music(c, identifier)
        Database.close(connection)
        return music[0]

    @staticmethod
    def get_music_playlists(id_music):
        connection = Database.connect()
        c = connection.cursor()
        playlists = PlaylistMusic.select_music(c, id_music)
        Database.close(connection)
        return playlists

    # Naming Rules -----------------------------------------------------------------------------------------------------

    @staticmethod
    def get_naming_rules():
        connection = Database.connect()
        c = connection.cursor()
        rules = NamingRules.select_all(c)
        Database.close(connection)
        return rules

    @staticmethod
    def new_naming_rule(replace, replace_by, priority):
        connection = Database.connect()
        c = connection.cursor()
        NamingRules.insert(c, replace, replace_by, priority)
        identifier = NamingRules.get_id_of_last_entry(c)
        Database.close(connection)
        return identifier[0]['id']

    @staticmethod
    def get_naming_rule(id_rule):
        connection = Database.connect()
        c = connection.cursor()
        rule = NamingRules.select(c, id_rule)
        Database.close(connection)
        return rule[0]

    @staticmethod
    def update_naming_rule(identifier, replace, replace_by, priority):
        connection = Database.connect()
        c = connection.cursor()
        NamingRules.update(c, identifier, replace, replace_by, priority)
        Database.close(connection)
        return "Naming Rule updated"

    @staticmethod
    def delete_naming_rule(identifier):
        connection = Database.connect()
        c = connection.cursor()
        NamingRules.delete(c, identifier)
        Database.close(connection)
        return "Naming Rule removed"

    # Channels ---------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_channels():
        connection = Database.connect()
        c = connection.cursor()
        rules = Channels.select_all(c)
        Database.close(connection)
        return rules

    @staticmethod
    def new_channel(channel, separator, artist_before_title):
        connection = Database.connect()
        c = connection.cursor()
        Channels.insert(c, channel, separator, artist_before_title)
        Database.close(connection)
        return "Channel added"

    @staticmethod
    def get_channel(id_channel):
        connection = Database.connect()
        c = connection.cursor()
        channel = Channels.select_channel(c, id_channel)
        Database.close(connection)
        if len(channel) == 0:
            return id_channel
        else:
            return channel[0]

    @staticmethod
    def update_channel(identifier, separator, artist_before_title):
        connection = Database.connect()
        c = connection.cursor()
        Channels.update(c, identifier, separator, artist_before_title)
        Database.close(connection)
        return "Channel updated"

    @staticmethod
    def delete_channel(identifier):
        connection = Database.connect()
        c = connection.cursor()
        Channels.delete(c, identifier)
        Database.close(connection)
        return "Channel removed"


# Requests -------------------------------------------------------------------------------------------------------------


class Playlists:
    @staticmethod
    def create(cursor):
        cursor.execute("CREATE TABLE Playlists (id text PRIMARY KEY, name text, uploader text, folder text)")

    @staticmethod
    def drop(cursor):
        cursor.execute("DROP TABLE IF EXISTS Playlists")

    @staticmethod
    def select_all(cursor):
        cursor.execute("SELECT * FROM Playlists")
        return cursor.fetchall()

    @staticmethod
    def select(cursor, identifier):
        cursor.execute("SELECT * FROM Playlists WHERE id = ?", (identifier,))
        return cursor.fetchall()

    @staticmethod
    def insert(cursor, identifier, name, uploader, folder):
        cursor.execute("INSERT INTO Playlists VALUES (?, ?, ?, ?)",
                       (identifier, name, uploader, folder))

    @staticmethod
    def update(cursor, identifier, name, uploader, folder):
        cursor.execute("UPDATE Playlists SET "
                       "name = ?, "
                       "uploader = ?, "
                       "folder = ? "
                       "WHERE "
                       "id = ?",
                       (name, uploader, folder, identifier))

    @staticmethod
    def delete(cursor, identifier):
        cursor.execute("DELETE FROM Playlists WHERE id = ?", (identifier,))


class Music:
    @staticmethod
    def create(cursor):
        cursor.execute("CREATE TABLE Music (id text PRIMARY KEY, "
                       # "name text, title text, artist text, channel text, upload_date date, new integer)")
                       "name text, title text, artist text, channel text, new integer)")

    @staticmethod
    def drop(cursor):
        cursor.execute("DROP TABLE IF EXISTS Music")

    @staticmethod
    def select_music(cursor, identifier):
        cursor.execute("SELECT * FROM Music WHERE id = ?", (identifier,))
        return cursor.fetchall()

    @staticmethod
    def select_new(cursor):
        cursor.execute("SELECT * FROM Music WHERE new = 'true'")
        return cursor.fetchall()

    @staticmethod
    # def insert(cursor, identifier, name, title, artist, channel, upload_date):
    def insert(cursor, identifier, name, title, artist, channel):
        cursor.execute("INSERT INTO Music VALUES (?, ?, ?, ?, ?, 'true')",
                       (identifier, name, title, artist, channel))

    @staticmethod
    def update(cursor, identifier, title, artist, new):
        cursor.execute("UPDATE Music SET "
                       "title = ?, "
                       "artist = ?, "
                       "new = ? "
                       "WHERE "
                       "id = ?",
                       (title, artist, new, identifier))

    @staticmethod
    def delete(cursor, identifier):
        cursor.execute("DELETE FROM Music WHERE id = ?", (identifier,))


class PlaylistMusic:
    @staticmethod
    def create(cursor):
        cursor.execute("CREATE TABLE Playlist_Music "
                       "(id INTEGER PRIMARY KEY AUTOINCREMENT, id_playlist text, id_music text)")

    @staticmethod
    def drop(cursor):
        cursor.execute("DROP TABLE IF EXISTS Playlist_Music")

    @staticmethod
    def select_playlist(cursor, id_playlist):
        cursor.execute("SELECT * FROM Playlist_Music WHERE id_playlist = ?", (id_playlist,))
        return cursor.fetchall()

    @staticmethod
    def select_music(cursor, id_music):
        cursor.execute("SELECT * FROM Playlist_Music WHERE id_music = ?", (id_music,))
        return cursor.fetchall()

    @staticmethod
    def count_playlist_music(cursor, id_playlist, id_music):
        cursor.execute("SELECT COUNT(*) FROM Playlist_Music "
                       "WHERE id_playlist = ? AND id_music = ?", (id_playlist, id_music))
        return cursor.fetchall()

    @staticmethod
    def insert(cursor, id_playlist, id_music):
        cursor.execute("INSERT INTO Playlist_Music (id_playlist, id_music) "
                       "VALUES (?, ?)", (id_playlist, id_music))

    @staticmethod
    def delete_playlist(cursor, id_playlist):
        cursor.execute("DELETE FROM Playlist_Music WHERE id_playlist = ?", (id_playlist,))


class Channels:
    @staticmethod
    def create(cursor):
        cursor.execute("CREATE TABLE Channels (channel text PRIMARY KEY, separator text, artist_before_title integer)")

    @staticmethod
    def drop(cursor):
        cursor.execute("DROP TABLE IF EXISTS Channels")

    @staticmethod
    def select_all(cursor):
        cursor.execute("SELECT * FROM  Channels")
        return cursor.fetchall()

    @staticmethod
    def select_channel(cursor, channel):
        cursor.execute("SELECT * FROM Channels WHERE channel = ?", (channel,))
        return cursor.fetchall()

    @staticmethod
    def insert(cursor, channel, separator, artist_before_title):
        cursor.execute("INSERT INTO Channels VALUES (?, ?, ?)",
                       (channel, separator, artist_before_title))

    @staticmethod
    def update(cursor, channel, separator, artist_before_title):
        cursor.execute("UPDATE Channels SET "
                       "separator = ?, "
                       "artist_before_title = ? "
                       "WHERE "
                       "channel = ?",
                       (separator, artist_before_title, channel))

    @staticmethod
    def delete(cursor, identifier):
        cursor.execute("DELETE FROM Channels WHERE channel = ?", (identifier,))


class NamingRules:
    @staticmethod
    def create(cursor):
        cursor.execute("CREATE TABLE NamingRules "
                       "(id INTEGER PRIMARY KEY AUTOINCREMENT, replace text, replace_by text, priority integer)")

    @staticmethod
    def drop(cursor):
        cursor.execute("DROP TABLE IF EXISTS NamingRules")

    @staticmethod
    def select_all(cursor):
        cursor.execute("SELECT * FROM NamingRules ORDER BY priority")
        return cursor.fetchall()

    @staticmethod
    def select(cursor, identifier):
        cursor.execute("SELECT * FROM NamingRules WHERE id = ?", (identifier,))
        return cursor.fetchall()

    @staticmethod
    def insert(cursor, replace, replace_by, priority):
        cursor.execute("INSERT INTO NamingRules (replace, replace_by, priority) "
                       "VALUES (?, ?, ?)", (replace, replace_by, priority))

    @staticmethod
    def get_id_of_last_entry(cursor):
        cursor.execute("SELECT id FROM NamingRules ORDER BY id DESC LIMIT 1")
        return cursor.fetchall()

    @staticmethod
    def update(cursor, identifier, replace, replace_by, priority):
        cursor.execute("UPDATE NamingRules SET "
                       "replace = ?, "
                       "replace_by = ?, "
                       "priority = ? "
                       "WHERE "
                       "id = ?",
                       (replace, replace_by, priority, identifier))

    @staticmethod
    def delete(cursor, identifier):
        cursor.execute("DELETE FROM NamingRules WHERE id = ?", (identifier,))
