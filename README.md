# YtMusicDownloader
YtMusicDownloader is a python service that downloads music from YouTube automatically. Service is manageable through an integrated API.  
YtMusicDownloader uses youtube-dl to download files. Shout-outs to them and [here](https://github.com/ytdl-org/youtube-dl)'s the project page.
To see features and usage of the API, refer to "YtMusicDownloader/docs/API User Guide.md". this document is also available on "/" once the web server is running. 
## Installation
You can run the service with Docker. Youtube-dl is integrated in the docker container.
### Docker
1. Build the docker container  
`sudo docker-compose build --no-cache`
2. Run the container  
`sudo docker-compose up`
### Set permissions
*If using a docker container, this might not be necessary.*
YtMusicDownloader actually needs sudoer privilege to modify permissions of the downloaded music.  
This is because youtube-dl needs to be executed as sudo to download videos and this results in the downloaded files being owned by root.
You also need sudo privilege to run the youtube-dl update command.  
Here's how to make it work:
Edit the /etc/sudoers file (`sudo nano /etc/sudoers) and add the following lines:  
`*username* ALL=(ALL:ALL) NOPASSWD:/usr/local/bin/youtube-dl -U`  
`*username* ALL=(ALL:ALL) NOPASSWD:/bin/chmod`  
`*username* ALL=(ALL:ALL) NOPASSWD:/bin/chown`  
What this does is that your user can now use these two commands with sudo without the need of enter the password.  
This is secure because you still need to be connected as the user to use the commands, and you have to enter the password to do so.  
It is only unsecure if you fear that someone physically uses your computer while you left with your session open.   
