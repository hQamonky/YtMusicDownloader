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
    bool_types = [('true', 'true'), ('false', 'false')]
    id = StringField('id')
    name = StringField('name')
    title = StringField('title')
    artist = StringField('artist')
    channel = StringField('channel')
    new = SelectField('new', choices=bool_types)


# Naming Rules ---------------------------------------------------------------------------------------------------------


@app.route('/ui/naming-rules')
def ui_naming_rules():
    # Declare the table
    class ItemTable(Table):
        id = Col('id')
        replace = Col('replace')
        replace_by = Col('replace_by')
        priority = Col('priority')
        # Add edit button
        edit = LinkCol('Edit', 'ui_edit_naming_rule', url_kwargs=dict(identifier='id'))
        # Add delete button
        delete = LinkCol('Delete', 'ui_delete_naming_rule', url_kwargs=dict(identifier='id'))

    # Get some data
    data = Controller.get_naming_rules()
    # Populate the table
    table = ItemTable(data)
    # Render html
    return render_template("naming_rules/naming_rules.html", table=table)


@app.route('/ui/naming-rules/new', methods=['GET', 'POST'])
def ui_new_naming_rule():
    form = NamingRuleForm(request.form)

    if request.method == 'POST' and form.validate():
        # Get form data
        class Args:
            replace = form.replace.data
            replace_by = form.replace_by.data
            priority = form.priority.data

        # save the rule
        Controller.new_naming_rule(Args())
        return redirect('/ui/naming-rules')

    return render_template('naming_rules/new_naming_rule.html', form=form)


@app.route('/ui/naming-rule/<identifier>', methods=['GET', 'POST'])
def ui_edit_naming_rule(identifier):
    # Get rule info
    naming_rule = Controller.get_naming_rule(identifier)
    form = NamingRuleForm(formdata=request.form, replace=naming_rule['replace'], replace_by=naming_rule['replace_by'],
                          priority=naming_rule['priority'])

    if naming_rule:
        if request.method == 'POST' and form.validate():
            # save edits
            class Args:
                replace = form.replace.data
                replace_by = form.replace_by.data
                priority = form.priority.data

            Controller.update_naming_rule(identifier, Args())
            return redirect('/ui/naming-rules')
        return render_template('naming_rules/edit_naming_rule.html', form=form, id=naming_rule['id'])


@app.route('/ui/naming-rule/<identifier>/delete', methods=['GET', 'POST'])
def ui_delete_naming_rule(identifier):
    # Get rule info
    naming_rule = Controller.get_naming_rule(identifier)
    form = NamingRuleForm(formdata=request.form)

    if naming_rule:
        if request.method == 'POST' and form.validate():
            # Delete rule
            Controller.delete_naming_rule(identifier)
            return redirect('/ui/naming-rules')
        return render_template('naming_rules/delete_naming_rule.html',
                               id=naming_rule['id'],
                               replace=naming_rule['replace'],
                               replace_by=naming_rule['replace_by'],
                               priority=naming_rule['priority'])


class NamingRuleForm(Form):
    replace = StringField('replace')
    replace_by = StringField('replace_by')
    priority = StringField('priority')


# Channels -------------------------------------------------------------------------------------------------------------


@app.route('/ui/channels')
def ui_channels():
    # Declare the table
    class ItemTable(Table):
        channel = Col('channel')
        separator = Col('separator')
        artist_before_title = Col('artist_before_title')
        # Add edit button
        edit = LinkCol('Edit', 'ui_edit_channel', url_kwargs=dict(identifier='channel'))
        # Add delete button
        delete = LinkCol('Delete', 'ui_delete_channel', url_kwargs=dict(identifier='channel'))

    # Get some data
    data = Controller.get_channels()
    # Populate the table
    table = ItemTable(data)
    # Render html
    return render_template("channels/channels.html", table=table)


@app.route('/ui/channel/new', methods=['GET', 'POST'])
def ui_new_channel():
    form = ChannelForm(request.form)

    if request.method == 'POST' and form.validate():
        # Get form data
        class Args:
            channel = form.channel.data
            separator = form.separator.data
            artist_before_title = form.artist_before_title.data

        # save the channel
        Controller.new_channel(Args())
        return redirect('/ui/channels')

    return render_template('channels/new_channel.html', form=form)


@app.route('/ui/channel/<identifier>', methods=['GET', 'POST'])
def ui_edit_channel(identifier):
    # Get channel info
    channel = Controller.get_channel(identifier)
    form = ChannelForm(formdata=request.form, separator=channel['separator'],
                       artist_before_title=channel['artist_before_title'])

    if channel:
        if request.method == 'POST' and form.validate():
            # save edits
            class Args:
                separator = form.separator.data
                artist_before_title = form.artist_before_title.data

            Controller.update_channel(identifier, Args())
            return redirect('/ui/channels')
        return render_template('channels/edit_channel.html', form=form, channel=channel['channel'])


@app.route('/ui/channel/<identifier>/delete', methods=['GET', 'POST'])
def ui_delete_channel(identifier):
    # Get channel info
    channel = Controller.get_channel(identifier)
    form = ChannelForm(formdata=request.form)

    if channel:
        if request.method == 'POST':
            # Delete channel
            Controller.delete_channel(identifier)
            return redirect('/ui/channels')
        return render_template('channels/delete_channel.html',
                               channel=channel['channel'],
                               separator=channel['separator'],
                               artist_before_title=channel['artist_before_title'])


class ChannelForm(Form):
    bool_types = [('true', 'true'), ('false', 'false')]
    channel = StringField('channel')
    separator = StringField('separator')
    artist_before_title = SelectField('artist_before_title', choices=bool_types)


# Configuration --------------------------------------------------------------------------------------------------------


@app.route('/ui/configuration', methods=['GET', 'POST'])
def ui_configuration():
    # Get playlist info
    configuration = Controller.get_configuration()
    form = ConfigurationForm(formdata=request.form,
                             download_interval=configuration['download_interval'],
                             use_custom_user=configuration['use_custom_user'],
                             separator=configuration['naming_format']['separator'],
                             artist_before_title=configuration['naming_format']['artist_before_title'])

    if configuration:
        if request.method == 'POST' and form.validate():
            # save edits
            class Args:
                download_interval = form.download_interval.data
                use_custom_user = form.use_custom_user.data
                separator = form.separator.data
                artist_before_title = form.artist_before_title.data
            args = Args()
            Controller.set_download_interval(args.download_interval)
            Controller.update_config_user(args.use_custom_user)
            Controller.update_config_naming_format(args)
            return redirect('/ui/home')
        return render_template('configuration.html', form=form)


class ConfigurationForm(Form):
    bool_types = [('true', 'true'), ('false', 'false')]
    download_interval = StringField('download_interval')
    use_custom_user = SelectField('use_custom_user', choices=bool_types)
    separator = StringField('separator')
    artist_before_title = SelectField('artist_before_title', choices=bool_types)
