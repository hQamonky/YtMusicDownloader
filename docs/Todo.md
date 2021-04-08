# Version 3.0
- Handle syncthing conflicts
    - Create method that deletes syncthing conflict files 
    - run method after each download
- Handle music archiving
    - Create ui to:
        - search the "Remove" playlist and display it's content
        - Validate button to run "removal"
    - Create methods in Controller to move music files to the archive folder
    - Add "archive folder path" to configuration
# Version 4.0
- Clean code (use object for database, etc)
- Handle errors and display error messages
- Create tests