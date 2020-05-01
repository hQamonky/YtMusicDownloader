# YtMusicDownloader-api
Manage, through this API, a daemon that automatically downloads music from YouTube playlists.
## Features
- Handle multiple playlists :
    - Add/Edit/Remove playlists
    - Set playlist download folder
    - Trigger playlist download
- Set time/occurrence of automatic download
- Handle newly downloaded music :
    - See list of downloaded music "not seen yet"
    - Rename music title and artiste manually
    - Set new music to "seen"
- Handle naming rule :
    - Add/Edit/Delete rule
    - Strings to delete or replace (ex: delete "[Official Music Video]" from title)
    - Set rule condition on channel
## Usage
All requests will have the `Application/json` header.  
All `POST` and `DELETE` requests will take a `json` as a body.  
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
        "title": "Best of Willy tracks 2020 part 2",
        "uploader": "William Herlicq",
        "uploader_id": "UCT8Y-bugDyR4ADHoQ-FOluw",
        "folder": "/home/qmk/Music/Best of WillyTracks"
    },{
        "id": "PLCVGGn6GhhDtHxCJcPNymXhCtyEisxERY",
        "title": "Best of Chill Music",
        "uploader": "William Herlicq",
        "uploader_id": "UCT8Y-bugDyR4ADHoQ-FOluw",
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
    "title": "Best of Willy tracks 2020 part 2",
    "uploader": "William Herlicq",
    "uploader_id": "UCT8Y-bugDyR4ADHoQ-FOluw",
    "folder": "/home/qmk/Music/Best of WillyTracks"
}
```
## `/playlist/<id>`
### `GET`  
*Response*  
- `404 Not found` if playlist does not exist
- `200 OK` on success  
```json
[
    {
        "_type": "playlist", 
        "entries": [
            {
                "_type": "url", 
                "url": "ftshNCG_RPk", 
                "ie_key": "Youtube", 
                "id": "ftshNCG_RPk", 
                "title": "Bad Computer - Riddle [Monstercat Release]"
            }, {
                "_type": "url",
                "url": "5S5zfXao-h0", 
                "ie_key": "Youtube", 
                "id": "5S5zfXao-h0", 
                "title": "Netrum - Colorblind (feat. Halvorsen) [NCS Release]"
            }
        ], 
        "id": "PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT", 
        "title": "Best of Willy tracks 2020 part 2", 
        "uploader": "William Herlicq", 
        "uploader_id": "UCT8Y-bugDyR4ADHoQ-FOluw", 
        "uploader_url": "https://www.youtube.com/channel/UCT8Y-bugDyR4ADHoQ-FOluw", 
        "extractor": "youtube:playlist", 
        "webpage_url": "https://www.youtube.com/playlist?list=PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT", 
        "webpage_url_basename": "playlist", 
        "extractor_key": "YoutubePlaylist",
        "folder": "/home/qmk/Music/Best of WillyTracks"
    }
]
```
### `POST`  
*Body*  
```json
{
    "id": "PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT",
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
        "artiste": "Bad Computer",
        "channel": "Monstercat: Uncaged",
        "upload_date": "13/04/2020",
        "folder": "/home/qmk/Music/Best of WillyTracks/",
        "new": "true"
    },
    {
        "id": "5S5zfXao-h0",
        "file_name": "Netrum - Colorblind (feat. Halvorsen) [NCS Release]",
        "title": "Colorblind (feat. Halvorsen)",
        "artiste": "Netrum",
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
    "artiste": "Bad Computer",
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
    "artiste": "Bad Computer",
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
        "channel": "all",
        "priority": "1"
    },
    {
        "id": "1",
        "replace": "u00e9",
        "replace_by": "é",
        "channel": "all",
        "priority": "2"
    },
    {
        "id": "2",
        "replace": " [Monstercat Release]",
        "replace_by": "",
        "channel": "Monstercat: Uncaged",
        "priority": "2"
    }
]
```
### `POST`
*Body*  
- List of rules with the following parameters :
    - `replace` *(string to replace)*.
    - `replace_by` *(new string that replaces old)*.
    - `channel` *(rule applies only if video comes from specified YT channel. Setting parameter to "all" will apply rule regardless of the channel)*.
    - `priority` *(in what order should the rules apply relatively to other rules, lowest number will apply first. Naming rules occur before naming format.)*
```json
{
    "replace": "‒",
    "replace_by": "-",
    "channel": "all",
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
    "channel": "all",
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
    "channel": "all",
    "priority": "1"
}
```
### `POST`
*Body*  
```json
{
    "replace": "‒",
    "replace_by": "-",
    "channel": "all",
    "priority": "1"
}
```
*Response*
- `201 Updated` on success   
```json
{
    "replace": "‒",
    "replace_by": "-",
    "channel": "all",
    "priority": "1"
}
```
### `DELETE`
*Response*  
- `404 Not found` if playlist does not exist
- `200 OK` on success 

## `/naming-formats`
### `GET`  
*Response*  
- `200 OK` on success  
Returns list of format rules.  
```json
[
    {
        "id": "0",
        "separator": " - ",
        "artiste_before_title": "true",
        "channel": "default"
    },
    {
        "id": "1",
        "separator": " - ",
        "artiste_before_title": "false",
        "channel": "Pegboard Nerds"
    }
]
```
### `POST`
*Body*  
- List of rules with the following parameters :
    - `separator` *(string that separates title and artist)*.
    - `artiste_before_title` *(`true` if artist name is before the title name in video name. Otherwise `false`)*.
    - `channel` *(rule applies only if video comes from specified YT channel. Setting parameter to "default" will apply rule if the channel cannot be found in annother rule)*.
```json
{
    "separator": " - ",
    "artiste_before_title": "true",
    "channel": "default"
}
```
*Response*  
- `201 Created` on success  
```json
{
    "id": "0",
    "separator": " - ",
    "artiste_before_title": "true",
    "channel": "default"
}
```

## `/naming-format/<id>`
### `GET`  
*Response*  
- `200 OK` on success  
```json
{
    "separator": " - ",
    "artiste_before_title": "true",
    "channel": "default"
}
```
### `POST`
*Body*  
```json
{
    "separator": " - ",
    "artiste_before_title": "true",
    "channel": "default"
}
```
*Response*  
- `201 Updated` on success  
```json
{
    "separator": " - ",
    "artiste_before_title": "true",
    "channel": "default"
}
```
### `DELETE`
*Response*  
- `404 Not found` if playlist does not exist
- `200 OK` on success 
