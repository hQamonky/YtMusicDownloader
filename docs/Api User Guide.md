# YtMusicDownloader-api
## Description
Manage, through this API, a daemon that automatically downloads music from YouTube playlists.
## Features
- Handle multiple playlists :
    - Add/Edit/Remove playlists
    - Set playlist link
    - Set playlist folder
    - Force playlist download
- Set time/occurrence of automatic download
- Handle newly downloaded music :
    - See downloaded music "not seen yet"
    - Set new music to "seen"
    - Rename music manually
- Set naming rule :
    - Depending on channel
    - String to delete (ex: "[Official Music Video]")
## Usage
### Playlists
`/playlists`
GET 
`/playlist/<id>`
GET 
POST
DELETE
`/playlist/<id>/download`
GET 
Get list of music that have not been downloaded yet.
POST
Trigger download.
### Music
`/music/new`
GET
Returns list of "not seen" music
`/music/<id>`
POST
- Rename a music.
- Move playlist
- Set "new" attribute to false
DELETE
This will actually archive the music. Meaning it will move the file to an "archive" folder.  
The path of the archive folder is set in the configuration and is not editable through the API (for security purposes). 
The music will be moved under "/path/to/archives/*artist*/".
### Download Occurrence
`/download-occurrence`
GET
POST
- Download occurrence
### Naming Rules
`/naming-rules`
GET
POST
- List of rules with the following parameters :
    - Channel *(rule applies only if video comes from specified YT channel. Setting parameter to "all" will 
    apply rule regardless of the channel)*.
    - Regex *(regex to apply)*.