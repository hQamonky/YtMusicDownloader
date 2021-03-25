# YtMusicDownloader-api
Manage, through this API, a daemon that automatically downloads music from YouTube playlists.
## Features
- Handle multiple playlists :
    - Add/Remove playlists
    - Edit playlists
    - Trigger playlist download
- Set interval time between each automatic download
- Handle newly downloaded music :
    - See list of downloaded music "not seen yet"
    - Rename music title and artist manually
    - Set new music to "seen"
- Handle title and artist naming :
    - Add/Edit/Delete rules
    - Strings replace (ex: replace " [Official Music Video]" by "")
    - Set title/artist format to apply depending on youtube channel 
    - Set title/artist default format to apply for new channels
## List of endpoints
- `/`
- `/configure`
- `/configuration/user`
- `/configuration/naming-format`
- `/factory-reset`
- `/auto-download`
- `/youtube-dl/update`
- `/playlists`
- `/playlists/download`
- `/playlist/<identifier>`
- `/playlist/<identifier>/download`
- `/music/new`
- `/music/<identifier>`
- `/naming-rules`
- `/naming-rule/<identifier>`
- `/channels`
- `/channel/<identifier>`
## Usage
All requests will have the `Application/json` header.  
All `POST` requests will take a `json` as a body.  
All responses will have the form :  
```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```
Subsequent response definitions will only detail the expected value of the `data field`.  
Also, they will only define the responses of `GET` request. Post requests usually return the full json object that was modified.  

## `/configuration`
### `GET`  
Get the configuration file.  
*Response*  
```json
{
    "version": "0.1", 
    "interval": "12",
    "use_custom_user": "false",
    "naming_format": {
        "separator": " - ", 
        "artist_before_title": "true"
    }
}
```

## `/configuration/user`
### `POST`  
Set if you want the downloaded files to be owned by the user that was set during the docker build.  
If you set as false, the files will be owned by root, but will be readable and writable by everyone.  
*Body*  
```json
{
    "use_custom_user": "true"
}
```

## `/configuration/naming-format`
### `POST`  
Set the default naming format for songs. The naming format is uses to determine the title and artist by using the name of the video.  
*Body*  
```json
{
    "separator": " - ", 
    "artist_before_title": "true"
}
```

## `/factory-reset`
### `POST`  
Reset configuration and database to default.  

## `/auto-download`
### `POST`  
Give an interval of time for when the service will automatically download all the playlists.  
The interval is defined in hours and the default is 12. Set it at -1 to disable it.  
The first download will occur in an amount of time equal to the "interval" value, starting from the execution of this command.  
*Body*  
```json
{
    "interval": "12"
}
```

## `/youtube-dl/update`
If you get an internal server error, updating youtube-dl might be a quick fix.  
If not, you'll have to wait for an update from qmk YtMusicDownloader.  

## `/playlists`
### `GET`  
Get information on the registered playlists in the database.  
*Response*  
```json
[
    {
        "id": "0",
        "youtube_id": "PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT",
        "name": "Best of Willy tracks",
        "uploader": "William Herlicq",
        "folder": "/Music/Best of WillyTracks"
    },{
        "id": "1",
        "youtube_id": "PLCVGGn6GhhDtHxCJcPNymXhCtyEisxERY",
        "name": "Best of Chill Music",
        "uploader": "William Herlicq",
        "folder": "/Music/Chill"
    }
]
```
### `POST`  
Register a playlist in the database.  
**Note that the root of the folder (here /Music) must match with the one that was configured during the docker run command of the setup!**  
*Body*  
```json
{
    "url": "https://www.youtube.com/playlist?list=PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT",
    "name": "Best of Willy tracks",
    "folder": "/Music/Best of WillyTracks"
}
```

## `/playlists/download`
*Response*  
### `POST`  
Trigger download of all registered playlists.   

## `/playlist/<identifier>`
### `POST`  
Edit a specified playlist.  
*Body*  
```json
{
    "url": "https://www.youtube.com/playlist?list=PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT",
    "name": "Best of Willy tracks",
    "folder": "/Music/Best of WillyTracks"
}
```
### `DELETE`
Remove a registered playlist from the database. Downloaded files from this playlist are not touched.  
If you re-register a removed playlist, it will re-download all the music (including those that were already downloaded).   

## `/playlist/<identifier>/download`
*Response*  
### `POST`  
Trigger download of the specified playlist.  

## `/music/new`
### `GET`  
Returns list of "not seen" music (where the "new" parameter equals "true").  
*Response*  
```json
[
    {
        "id": "ftshNCG_RPk",
        "file_name": "Bad Computer - Riddle [Monstercat Release]",
        "title": "Riddle",
        "artist": "Bad Computer",
        "channel": "Monstercat: Uncaged",
        "upload_date": "13/04/2020",
        "folders": ["/Music/Best of WillyTracks/"],
        "new": "true"
    },
    {
        "id": "5S5zfXao-h0",
        "file_name": "Netrum - Colorblind (feat. Halvorsen) [NCS Release]",
        "title": "Colorblind (feat. Halvorsen)",
        "artist": "Netrum",
        "channel": "NoCopyrightSounds",
        "upload_date": "14/04/2020",
        "folder": "/Music/Best of WillyTracks/",
        "new": "true"
    }
]
```

## `/music/<identifier>`
### `POST`  
- Rename a musics title and artist.  
Not hat every parameter is required.  
*Body*  
```json
{
    "title": "Riddle",
    "artist": "Bad Computer",
    "new": "false"
}
```

## `/naming-rules`
### `GET`  
Returns the list of rules. These rules are applied in order to help to determine the title and artist from the name of the video.  
It is useful to remove strings like " (Official Video)" or handle special characters.   
*Response*  
```json
[
    {
        "id": "0",
        "replace": "‒",
        "replace_by": "-",
        "priority": "1"
    },
    {
        "id": "1",
        "replace": "u00e9",
        "replace_by": "é",
        "priority": "2"
    },
    {
        "id": "2",
        "replace": " [Monstercat Release]",
        "replace_by": "",
        "priority": "2"
    }
]
```
### `POST`
*Body*  
Add a new rule with the following parameters :  
    - `replace` *(string to replace)*.  
    - `replace_by` *(new string that replaces old)*.  
    - `priority` *(in what order should the rules apply relatively to other rules, lowest number will apply first. Naming rules occur before naming format.)*  
```json
{
    "replace": "‒",
    "replace_by": "-",
    "priority": "1"
}
```

## `/naming-rule/<identifier>`
### `GET`  
Get the specified rule.
*Response*  
```json
{
    "replace": "‒",
    "replace_by": "-",
    "priority": "1"
}
```
### `POST`
Edit the specified rule.  
*Body*  
```json
{
    "replace": "‒",
    "replace_by": "-",
    "priority": "1"
}
```
### `DELETE`
Delete the specified rule.  

## `/channels`
### `GET`  
Get the list of channels registered in the database. For each channel there is a naming format that applies.  
The first time that a video is downloaded from a channel, the channel is automatically registered with the default naming rule defined in the configuration file (accessible and manageable through the /configuration.naming-rule endpoint).  
*Response*  
```json
[
    {
        "channel": "Monstercat: Uncaged",
        "separator": " - ",
        "artist_before_title": "true"
    },
    {
        "channel": "Pegboard Nerds",
        "separator": " - ",
        "artist_before_title": "false"
    }
]
```
### `POST`
*Body*  
- List of rules with the following parameters :
    - `channel` *(rule applies only if video comes from specified YT channel)*
    - `separator` *(string that separates title and artist)*
    - `artist_before_title` *(`true` if artist name is before the title name in video name. Otherwise `false`)*
```json
{
    "channel": "Monstercat: Uncaged",
    "separator": " - ",
    "artist_before_title": "true"
}
```

## `/channel/<identifier>`
### `GET`  
Get the specified channel.  
*Response*  
```json
{
    "channel": "Monstercat: Uncaged",
    "separator": " - ",
    "artist_before_title": "true"
}
```
### `POST`
Edit the naming format for the specified channel.  
*Body*  
```json
{
    "separator": " - ",
    "artist_before_title": "true"
}
```
### `DELETE`
Remove a channel from the database.  

