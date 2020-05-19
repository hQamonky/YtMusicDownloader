from wtforms import Form, StringField, SelectField
from flask import render_template, request, redirect
from flask_table import Table, Col, LinkCol
from src.endpoints import Controller
from src.endpoints import app


# Front End ------------------------------------------------------------------------------------------------------------


@app.route('/ui/home')
def ui_home():
    return render_template("home.html")


# Playlists ------------------------------------------------------------------------------------------------------------


@app.route('/ui/playlists')
def ui_playlists():
    # Declare the table
    class ItemTable(Table):
        id = Col('id')
        name = Col('name')
        uploader = Col('uploader')
        folder = Col('folder')
        # Add edit button
        edit = LinkCol('Edit', 'ui_edit_playlist', url_kwargs=dict(identifier='id'))
        # Add delete button
        delete = LinkCol('Delete', 'ui_delete_playlist', url_kwargs=dict(identifier='id'))
        # Add download button
        download = LinkCol('Download', 'ui_download_playlist', url_kwargs=dict(identifier='id'))

    # Get some data
    data = Controller.get_playlists()
    # Populate the table
    table = ItemTable(data)
    # Render html
    return render_template("playlists/playlists.html", table=table)


@app.route('/ui/playlist/new', methods=['GET', 'POST'])
def ui_new_playlist():
    form = PlaylistForm(request.form)

    if request.method == 'POST' and form.validate():
        # Get form data
        class Args:
            url = form.url.data
            folder = form.folder.data
        # save the playlist
        Controller.new_playlist(Args())
        return redirect('/ui/playlists')

    return render_template('playlists/new_playlist.html', form=form)


@app.route('/ui/playlist/<identifier>', methods=['GET', 'POST'])
def ui_edit_playlist(identifier):
    # Get playlist info
    playlist = Controller.get_playlist(identifier)
    form = PlaylistForm(formdata=request.form, folder=playlist['folder'])

    if playlist:
        if request.method == 'POST' and form.validate():
            # save edits
            class Args:
                folder = form.folder.data
            Controller.update_playlist(identifier, Args())
            return redirect('/ui/playlists')
        return render_template('playlists/edit_playlist.html', form=form, id=playlist['id'], name=playlist['name'],
                               uploader=playlist['uploader'])


@app.route('/ui/playlist/<identifier>/delete', methods=['GET', 'POST'])
def ui_delete_playlist(identifier):
    # Get playlist info
    playlist = Controller.get_playlist(identifier)
    form = PlaylistForm(formdata=request.form)

    if playlist:
        if request.method == 'POST' and form.validate():
            # Delete playlist
            Controller.delete_playlist(identifier)
            return redirect('/ui/playlists')
        return render_template('playlists/delete_playlist.html', id=playlist['id'], name=playlist['name'],
                               uploader=playlist['uploader'], folder=playlist['folder'])


@app.route('/ui/playlist/<identifier>/download', methods=['GET'])
def ui_download_playlist(identifier):
    # Get playlist info
    playlist = Controller.get_playlist(identifier)

    if playlist:
        # Download playlist
        logs = Controller.download_playlist(identifier)
        return render_template('playlists/download_playlist.html', logs=logs, id=playlist['id'], name=playlist['name'],
                               uploader=playlist['uploader'], folder=playlist['folder'])


class PlaylistForm(Form):
    url = StringField('url')
    folder = StringField('folder')


# Music ----------------------------------------------------------------------------------------------------------------


@app.route('/ui/music/new')
def ui_new_music():
    # Declare the table
    class ItemTable(Table):
        id = Col('id')
        name = Col('name')
        title = Col('title')
        artist = Col('artist')
        channel = Col('channel')
        new = Col('new')
        # Add edit button
        edit = LinkCol('Edit', 'ui_edit_music', url_kwargs=dict(identifier='id'))

    # Get some data
    data = Controller.get_new_music()
    # Populate the table
    table = ItemTable(data)
    # Render html
    return render_template("music/new_music.html", table=table)


@app.route('/ui/music/<identifier>', methods=['GET', 'POST'])
def ui_edit_music(identifier):
    # Get music info
    music = Controller.get_music(identifier)
    form = MusicForm(formdata=request.form, title=music['title'], artist=music['artist'],
                     new=music['new'])

    if music:
        if request.method == 'POST' and form.validate():
            # save edits
            class Args:
                title = form.title.data
                artist = form.artist.data
                new = form.new.data
            Controller.update_music(identifier, Args())
            return redirect('/ui/music/new')
        return render_template('music/edit_music.html', form=form,
                               id=music['id'],
                               name=music['name'],
                               title=music['title'],
                               artist=music['artist'],
                               channel=music['channel'],
                               new=music['new'])


class MusicForm(Form):
    bool_types = [('1', '1'), ('0', '0')]
    id = StringField('id')
    name = StringField('name')
    title = StringField('title')
    artist = StringField('artist')
    channel = StringField('channel')
    # new = StringField('new')
    new = SelectField('new', choices=bool_types)
