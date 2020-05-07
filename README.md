# YtMusicDownloader
YtMusicDownloader is a python service that downloads music from YouTube automatically. Service is manageable through an integrated API.  
YtMusicDownloader uses youtube-dl to download files. Shout-outs to them and [here](https://github.com/ytdl-org/youtube-dl)'s the project page.
To see features and usage of the API, refer to "YtMusicDownloader/docs/API User Guide.md". this document is also available on "/" once the web server is running. 
## Installation
You can run the service with Docker. Youtube-dl is integrated in the docker container.
You must first clone the project from github.
### Download project 
You can use any method you want but I will show here how to do it from the linux terminal (using a debian based system).
#### Install git
`sudo apt update`  
`sudo apt install git-core`
#### Clone project
`cd ~/Downloads`  
`git clone https://github.com/hQamonky/YtMusicDownloader.git`  
### Docker
If you want to set download folder outside of the container, you need to set it up yourself.  
Otherwise you'll have to set the relative path.
1. Build the docker container  
`sudo docker-compose build --no-cache`
2. Run the container  
`sudo docker-compose up`
### Without docker
You will need to set up your environment. Here's how to do it.
#### Linux (debian based system)
##### Install youtube-dl 
This part was copied from the [youtube-dl documentation]https://github.com/ytdl-org/youtube-dl.  
`sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl`  
`sudo chmod a+rx /usr/local/bin/youtube-dl`  
##### Install pip and virtiualenv
`sudo apt install python3-pip virtualenv`  
##### Create virtual environment
Open a terminal and navigate to the location where you have downloaded the project.  
`cd ~/Downloads`  
Create the environment with :  
`virtualenv YtMusicDownloader`  
Open the folder.  
`cd YtMusicDownloader`  
Activate the Python virtual environment :  
`source bin/activate`  
Run the service :  
`sudo  python3 run.py`
#### Windows / Mac OS
If you don't use Docker, it will most likely only work on Linux (but maybe I'm wrong, it's a python project after all).