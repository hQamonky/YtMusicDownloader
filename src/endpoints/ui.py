from wtforms import Form, StringField, SelectField
from flask import render_template, request, redirect
from flask_table import Table, Col, LinkCol
from src.endpoints import Controller
from src.endpoints import app


# Front End ------------------------------------------------------------------------------------------------------------


@app.route('/ui/home')
def ui_home():
    return render_template("home.html")


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


class PlaylistForm(Form):
    url = StringField('url')
    folder = StringField('folder')


@app.route('/ui/music/new')
def ui_new_music():
    return render_template("playlists/new_music.html")
