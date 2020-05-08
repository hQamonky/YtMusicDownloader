# YtMusicDownloader
YtMusicDownloader is a python service that downloads music from YouTube automatically. Service is manageable through an integrated API.  
YtMusicDownloader uses youtube-dl to download files. Shout-outs to them and [here](https://ytdl-org.github.io/youtube-dl/) is their website.  
To see features and usage of the API, refer to ["YtMusicDownloader/docs/API User Guide.md"](https://github.com/hQamonky/YtMusicDownloader/blob/master/docs/Api%20User%20Guide.md). this document is also available on "/" once the web server is running. 
# Installation
Requirement: This app is wrapped in a docker container, and so you have to use docker.  
## Linux (debian based)
### 1. Download the project from Github
> 1. Create a folder  
> `sudo mkdir /opt/qmk`
> 2. Go to the folder location  
> `cd /opt/qmk`
> 3. Download the project from GitHub  
> `git clone https://github.com/hQamonky/YtMusicDownloader.git`
>  
You can of course do this manually if you prefer: Download zip file form github and unzip it into `/opt/qmk`.  
### 2. Install Docker
> 1. In update system  
> `sudo apt update`  
> 2. Install requirements  
> `sudo apt install apt-transport-https ca-certificates curl software-properties-common`  
> 3. Install Docker package  
> `sudo snap install docker`  
>
If snap is not installed, install it with `sudo apt install snapd`.  
### 3. Load the docker image
`sudo docker load < /opt/YtMusicDownloader/qmk_yt_music_dl_v1.0.tar`  
## Mac OS and Newbies (Windows 10)
### 1. Download the project from Github
Create a folder where you want the program to run (typically /opt/qmk on Mac OS and C:\\Program Files\qmk on Windows).  
Download the project from [GitHub](https://github.com/hQamonky/YtMusicDownloader/archive/master.zip) and extract the zip file in the folder you just created.  
### 2. Install Docker
Follow the [docker documentation](https://docs.docker.com/).
### 3. Load the docker image
Open a terminal at the location of your folder and run:  
`docker load < YtMusicDownloader/qmk_yt_music_dl_v1.0.tar`  
# Usage
In this part, there are only docker commands and it is by consequence the same regardless of the OS.  
The only difference is that on Linux you have to run them as sudo, but on other systems you don't.
## Start the program
Use the command:  
`sudo docker run -p 8092:8080 -v /opt/YtMusicDownloader:/usr/src/app -v /home/qmk/Music:/Music -d --name qmk_yt_music_dl qmk_yt_music_dl:latest`  
Here you can customize this command if you want:  
- `8092` is the port you will be using to access the API.  
- `-v` enables the docker container to access a folder on the host machine.  
    - `-v /opt/YtMusicDownloader:/usr/src/app` is required and cannot be changed.  
    - `-v /home/qmk/Music:/Music` however can be used to set a folder where you want the app to output the downloads. You can even add more folders if you want.  
- The `-d` option makes the container run in the background and it gives you the id of the container.  
You can omit this option if you want to run the app in the foreground.  
- The `--name qmk_ytmusicdl` option gives a name to the container. It is optional but useful because we can use the name instead of the id of the container for the following commands.   
## Stop the  program
First you need to get the id of the container that is currently running. If you wrote down the id given by the previous command, you can use it. Or, if you gave it a name, you can use the name instead. Otherwise here's how to get it back:  
`sudo docker ps`  
This command lists the running docker containers.  
In the ID column is where you will find what we need.  
Then stop the container with:  
`sudo docker stop container_id` (replace *container_id* with the id (or name) you just retrieved)  
# Update
Unfortunately, there is no "simple" update process, you basically have to do the whole installation process again :)  
Well not everything actually, you already have installed docker, so you just have to:  
> 1. Download latest version from GitHub: `cd /opt/qmk && git clone https://github.com/hQamonky/YtMusicDownloader.git`
> 2. Load the docker image with `sudo docker load < /opt/YtMusicDownloader/qmk_yt_music_dl_v1.0.tar`  
> 
Then use the new image the same way as previously described (with `run` and `stop` commands).  
# Go a little further
I suggest that you create shortcuts to handle the docker commands.
## Linux (debian based)
### Create aliases
Create file `gedit ~/.bash_aliases` and insert the following:
``` bash
# qmk software
alias ytmusicdl-start="sudo docker run -p 8092:8080 -v /opt/YtMusicDownloader:/usr/src/app -v /home/qmk/Music:/Music -d --name qmk_yt_music_dl qmk_yt_music_dl:latest"  
alias ytmusicdl-stop="sudo docker stop qmk_yt_music_dl"  
```
Apply your changes with `source ~/.bash_aliases`.  
### Make system not ask for sudo password
Edit the file `sudo gedit /etc/sudoers` and add the following line at the end of the file:  
``` bash
qmk ALL=(ALL:ALL) NOPASSWD:/snap/bin/docker
```
### Create desktop launcher
Create file `sudo gedit /usr/share/applications/qmk_yt_music_downloader.desktop` and insert the following:  
``` bash
[Desktop Entry]  
Version = 1.0  
Type = Application  
Terminal = false  
Name = QMK YT Music Downloader  
Exec = ytmusicdl-start %f  
Icon = /opt/YtMusicDownloader/icon.png  
Categories = Application;  
```
Create an icon and rename/copy it to `/opt/YtMusicDownloader/icon.png`.  
If you want to have a terminal open when running the app, remove the `%f` on the "Exec" line.  
Apply changes with `sudo update-desktop-database`.  
You could also create a stop launcher if you want. I mean, be creative, do whatever.   