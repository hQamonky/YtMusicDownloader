# Version 2.1
- Handle real playlists:
    - Dissociate id and youtube id + add custom playlist names
    - Handle Mopidy playlists (create a "mopidy" folder)
- Handle music archiving
    - Create ui to:
        - search the "Remove" playlist and display it's content
        - Validate button to run "removal"
    - Create methods in Controller to move music files to the archive folder
    - Add "archive folder path" to configuration
# Version 3.0
- Clean code (use object for database, etc)
- Handle errors and display error messages
- Create tests