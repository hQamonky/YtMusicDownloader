# YtMusicDownloader-api
Manage, through this API, a daemon that automatically downloads music from YouTube playlists.
## Features
- Handle multiple playlists :
    - Add/Remove playlists
    - Edit playlist download folder
    - Trigger playlist download
- Set time/occurrence of automatic download
- Handle newly downloaded music :
    - See list of downloaded music "not seen yet"
    - Rename music title and artist manually
    - Set new music to "seen"
- Handle title and artist naming :
    - Add/Edit/Delete rules
    - Strings replace (ex: replace " [Official Music Video]" by "")
    - Set title/artist format to apply depending on channel on channel
    - Set title/artist default format to apply
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
## `/playlists`
### `GET`  
*Response*  
- `200 OK` on success  
```json
[
    {
        "id": "PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT",
        "name": "Best of Willy tracks 2020 part 2",
        "uploader": "William Herlicq",
        "folder": "/home/qmk/Music/Best of WillyTracks"
    },{
        "id": "PLCVGGn6GhhDtHxCJcPNymXhCtyEisxERY",
        "name": "Best of Chill Music",
        "uploader": "William Herlicq",
        "folder": "/home/qmk/Music/Chill"
    }
]
```
### `POST`  
*Body*  
```json
{
    "url": "https://www.youtube.com/playlist?list=PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT",
    "folder": "/home/qmk/Music/Best of WillyTracks"
}
```
*Response*  
- `201 Created` on success  
```json
{
    "id": "PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT",
    "name": "Best of Willy tracks 2020 part 2",
    "uploader": "William Herlicq",
    "folder": "/home/qmk/Music/Best of WillyTracks"
}
```
## `/playlist/<identifier>`
### `POST`  
*Body*  
```json
{
    "folder": "/home/qmk/Music/Best of WillyTracks"
}
```
*Response*  
- `201 Created` on success  
```json
{
    "id": "PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT",
    "title": "Best of Willy tracks 2020 part 2",
    "uploader": "William Herlicq",
    "uploader_id": "UCT8Y-bugDyR4ADHoQ-FOluw",
    "folder": "/home/qmk/Music/Best of WillyTracks"
}
```
### `DELETE`
*Response*  
- `404 Not found` if playlist does not exist
- `200 OK` on success  

## `/playlist/<id>/download`
*Response*  
### `POST`  
Trigger download.  
*Response*  
- `201 Downloaded` on success  

## `/download-occurrence`
### `GET`  
*Response*  
- `200 OK` on success  
Returns a list of times (of the day) when the download is triggered automatically. The time format is `HH:mm` (in 24h). Receiving an empty array means that the automatic download is disabled.
Otherwise, the download is always triggered every day.
```json
[
    {
        "time": "00:00"
    },{
        "time": "12:00"
    }
]
```

### `POST`
*Body*  
Set a list of times (of the day) when you want the download to be triggered automatically.  
The time format is `HH:mm` (in 24h).
Sending an empty array will disable the automatic download.
Otherwise, the download is always triggered every day and it cannot be changed.
```json
[
    {
        "time": "00:00"
    },{
        "time": "12:00"
    }
]
```
*Response*  
- `201 Updated` on success  
```json
[
    {
        "time": "00:00"
    },{
        "time": "12:00"
    }
]
```

## `/music/new`
### `GET`  
*Response*  
- `200 OK` on success  
Returns list of "not seen" music.  
```json
[
    {
        "id": "ftshNCG_RPk",
        "file_name": "Bad Computer - Riddle [Monstercat Release]",
        "title": "Riddle",
        "artist": "Bad Computer",
        "channel": "Monstercat: Uncaged",
        "upload_date": "13/04/2020",
        "folders": ["/home/qmk/Music/Best of WillyTracks/"],
        "new": "true"
    },
    {
        "id": "5S5zfXao-h0",
        "file_name": "Netrum - Colorblind (feat. Halvorsen) [NCS Release]",
        "title": "Colorblind (feat. Halvorsen)",
        "artist": "Netrum",
        "channel": "NoCopyrightSounds",
        "upload_date": "14/04/2020",
        "folder": "/home/qmk/Music/Best of WillyTracks/",
        "new": "true"
    }
]
```
## `/music/<id>`
### `POST`  
*Body*  
- Rename a music.  
- Set "new" attribute.  
```json
{
    "title": "Riddle",
    "artist": "Bad Computer",
    "new": "false"
}
```
*Response*  
- `201 Downloaded` on success  
```json
{
    "id": "ftshNCG_RPk",
    "file_name": "Bad Computer - Riddle [Monstercat Release]",
    "title": "Riddle",
    "artist": "Bad Computer",
    "channel": "Monstercat: Uncaged",
    "upload_date": "13/04/2020",
    "folder": "/home/qmk/Music/Best of WillyTracks/",
    "new": "false"
}
```

## `/naming-rules`
### `GET`  
*Response*  
- `200 OK` on success  
Returns list of rules.  
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
- List of rules with the following parameters :
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
*Response*  
- `201 Created` on success   
```json
{
    "id": "0",
    "replace": "‒",
    "replace_by": "-",
    "priority": "1"
}
```

## `/naming-rule/<id>`
### `GET`  
*Response*  
- `200 OK` on success   
```json
{
    "replace": "‒",
    "replace_by": "-",
    "priority": "1"
}
```
### `POST`
*Body*  
```json
{
    "replace": "‒",
    "replace_by": "-",
    "priority": "1"
}
```
*Response*
- `201 Updated` on success   
```json
{
    "replace": "‒",
    "replace_by": "-",
    "priority": "1"
}
```
### `DELETE`
*Response*  
- `404 Not found` if rule does not exist
- `200 OK` on success 

## `/channels`
### `GET`  
*Response*  
- `200 OK` on success  
Returns list of channels with title/artist renaming format rules.  
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
    - `channel` *(rule applies only if video comes from specified YT channel.)*.
    - `separator` *(string that separates title and artist)*.
    - `artist_before_title` *(`true` if artist name is before the title name in video name. Otherwise `false`)*.
```json
{
    "channel": "Monstercat: Uncaged",
    "separator": " - ",
    "artist_before_title": "true"
}
```
*Response*  
- `201 Created` on success  
```json
{
    "channel": "Monstercat: Uncaged",
    "separator": " - ",
    "artist_before_title": "true"
}
```

## `/channel/<id>`
### `GET`  
*Response*  
- `200 OK` on success  
```json
{
    "channel": "Monstercat: Uncaged",
    "separator": " - ",
    "artist_before_title": "true"
}
```
### `POST`
*Body*  
```json
{
    "separator": " - ",
    "artist_before_title": "true"
}
```
*Response*  
- `201 Updated` on success  
```json
{
    "channel": "Monstercat: Uncaged",
    "separator": " - ",
    "artist_before_title": "true"
}
```
### `DELETE`
*Response*  
- `404 Not found` if channel does not exist
- `200 OK` on success 
