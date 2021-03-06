# YtMusicDownloader
YtMusicDownloader is a python service that downloads music from YouTube automatically. The service is manageable through an integrated API. In case you don't want to use a client that uses the API, you can also use the service through the integrated web interface accessible from the /ui/home endpoint.  
YtMusicDownloader uses youtube-dl to download files. Shout-outs to them and [here](https://ytdl-org.github.io/youtube-dl/) is their website.  
To see features and usage of the API, refer to ["YtMusicDownloader/docs/API User Guide.md"](https://github.com/hQamonky/YtMusicDownloader/blob/master/docs/Api%20User%20Guide.md). this document is also available on "/" once the web server is running.  
The project integrates docker and the simplest way to use it is to clone the whole project and use docker. This guide will go over on how to do this, but you can refer to the [docker documentation](https://docs.docker.com/) for any problems or if you want to configure more advanced stuff yourself.
# Automatic Installation
The automatic installation is just a script that runs the default commands from the manual installation.  
Note that if you run into problems, or you want to personalize your installation, you will have to go through the manual installation. 
## Linux (Debian based), Raspbian & Mac OS
### From terminal
Linux (but not Raspbian)   
> `wget -P ~/Downloads https://raw.githubusercontent.com/hQamonky/YtMusicDownloader/develop/installers/debian_installer.sh`  
> `chmod +x ~/Downloads/debian_installer.sh`  
> `~/Downloads/debian_installer.sh`  

Raspbian  
> `wget -P ~/Downloads https://raw.githubusercontent.com/hQamonky/YtMusicDownloader/develop/installers/raspbian_installer.sh`  
> `chmod +x ~/Downloads/raspbian_installer.sh`  
> `~/Downloads/raspbian_installer.sh`  
  
Mac OS  
> `wget -P ~/Downloads https://raw.githubusercontent.com/hQamonky/YtMusicDownloader/develop/installers/mac_installer.sh`  
> `chmod +x ~/Downloads/mac_installer.sh`  
> `~/Downloads/mac_installer.sh`  

### From GUI
Open on the following link that matches your operating system:  
- [Linux (debian based)](https://raw.githubusercontent.com/hQamonky/YtMusicDownloader/master/installers/debian_installer.sh)  
- [Raspbian](https://raw.githubusercontent.com/hQamonky/YtMusicDownloader/master/installers/raspbian_installer.sh)  
- [Mac OS](https://raw.githubusercontent.com/hQamonky/YtMusicDownloader/master/installers/mac_installer.sh)  

Then, right click anywhere on the page and click "Save as...".  
Open a terminal where you downloaded the file.  
Make the script executable: `chmod +x your_installer.sh`  
Finally run the script.  
## Windows 10  
### Download the installation script  
Open on the following link: https://raw.githubusercontent.com/hQamonky/YtMusicDownloader/master/installers/windows_installer.bat  
Then, right click anywhere on the page and click "Save as...".  
Save the file but without the ".txt" extension! Keep the ".bat" extension.  
### Run the script as administrator 
Navigate to where you've downloaded the script and do Right Click -> Run as administrator.  
# Manual Installation
## 1. Install Docker
### Linux (debian based)
> 1. Update your system  
> `sudo apt update`  
> 2. Install requirements  
> `sudo apt install apt-transport-https ca-certificates curl software-properties-common`  
> 3. Install Docker package  
> `sudo snap install docker`  
>
If snap is not installed, install it with `sudo apt install snapd`.  
### Raspbian
> 1. Update your system  
> `sudo apt update`  
> 2. Get docker  
> `curl -sSL https://get.docker.com | sh`
> 3. Add user to docker group if you don't want to use sudo (needs reboot) 
> `sudo usermod -aG docker pi`
> 4. Install requirements
> `sudo apt-get install -y libffi-dev libssl-dev`
> `sudo apt-get install -y python3 python3-pip
> `sudo apt-get remove python-configparser`
> 5. Install docker-compose (we won't need it though)
> `sudo pip3 install docker-compose`

### Mac OS & Windows 10
Follow the [docker documentation](https://docs.docker.com/).
## 2. Download the project from Github
### Linux & Mac OS
> 1. Create a folder  
> `mkdir ~/qmk`
> 2. Download the project from GitHub  
> `git -C ~/qmk clone https://github.com/hQamonky/YtMusicDownloader.git`
>  
You can of course do this manually if you prefer: Download zip file form github and unzip it into `~/qmk`.  
### Windoesn't 10
> 1. Open the file explorer and go to C:\\Program Files\.  
> Create a folder names "qmk".  
> 2. Open the folder and do a "Shift+Right Click" -> "Open PowerShell window here".  
> Run the command `git clone https://github.com/hQamonky/YtMusicDownloader.git`   
> You can do this manually if you prefer: Download zip file form github and unzip it into C:\\Program Files\qmk\.  
## 3. Build the docker image
Build the image: `sudo docker build --no-cache -t qmk_yt_music_dl ~/qmk/YtMusicDownloader`  
For noob... erhum.. I mean Windows users, replace `~/qmk/YtMusicDownloader` by `C:\\Program Files\qmk\YtMusicDownloader`.  
You can add the `--build-arg` flag with the `user_id` and/or `group_id` arguments. This will enable you to access the downloaded file without needing root permissions.  
By default, the user_id is set to 1000 and the group_id equals the user_id.  
For example: `sudo docker build --build-arg user_id=1000 --no-cache -t qmk_yt_music_dl ~/qmk/YtMusicDownloader`, you have to replace `1000` by the id of your current user.  
To get this information, run `id` in a terminal, your user id is the uid. You can also set the group id by using the gid value.  
## 4. Run the image to create a container
Use the command:  
`sudo docker run -p 8092:8080 -v ~/qmk/YtMusicDownloader:/usr/src/app -v ~/Music:/Music -d --name qmk_ymd qmk_yt_music_dl`  
Here you can customize this command if you want:  
> - `8092` is the port you will be using to access the API.  
> - `-v` enables the docker container to access a folder on the host machine.  
>     - `-v ~/qmk/YtMusicDownloader:/usr/src/app` is required and cannot be changed.  
>     - `-v ~/Music:/Music` Here you can change to the path that you want.  
>     This option can be used to set a folder where you want the app to output the downloads. You can also add more folders with more -v flags if you want.    
> - The `-d` option makes the container run in the background and it gives you the id of the container.  
> You can omit this option if you want to run the app in the foreground.  
> - The `--name qmk_ymd` option gives a name to the container, you can name it whatever you want. It is optional but we will use it for starting and stopping the container.  
  
Once you have executed this command, the container will be started. Stop it with `sudo docker stop qmk_ymd`.
# Usage
## Start the program   
Simply run: `sudo docker start qmk_ymd`
## Stop the  program
Just run `sudo docker stop qmk_ymd`.  
If you have any problem, like you don't remember the name you gave it or something, here's how to deal with it.  
First display the information of the running containers with `sudo docker ps`.   
Write down the container id or the name of your container.  
Then stop the container with:  
`sudo docker stop container_id` (replace *container_id* with the id (or name) you just retrieved)  
You can also use the `docker kill` command, refer to the docker documentation for more information on that.  
## Using the web interface
The service can be used by using the simple web interface that it integrates.  
This interface is accessible from the /ui/home endpoint. From there you will have all the links to other pages of the gui.  
# Update
Unfortunately, there is no "simple" update process, you basically have to do the whole installation process again :)  
Well not everything actually, you already have installed docker and setup the container. So depending on the update, might not need to rebuild the docker container.  
**Be aware that the following steps might (normally should not) overwrite your data. If you don't want to lose it, make a backup of ytMusicDownloader.db and of configuration.json from ~/qmk/YtMusicDownloader/src/.**     
> 1. Update the project from GitHub: `git -C ~/qmk/YtMusicDownloader pull`  
> 2. Restart your container: `sudo docker restart qmk_ymd`  
If this works, you're good and you don't need to go any further.  
If it doesn't it means that you have to rebuild the docker container and do a "full update". So continue with the following steps.  
> 3. Remove the docker container: `sudo docker container rm -f qmk_ymd`  
> 4. Build the image: `sudo docker build --no-cache -t qmk_yt_music_dl ~/qmk/YtMusicDownloader` (*you can omit the --no-cache flag to go faster, but consider that it might cause problems*)  
> 5. Run the image: `sudo docker run -p 8092:8080 -v ~/qmk/YtMusicDownloader:/usr/src/app -v ~/Music:/Music -d --name qmk_ymd qmk_yt_music_dl`  
# Go a little further
I suggest that you create shortcuts to handle the docker commands.  
## Linux (might also work on Mac OS)
### Create update scripts
#### Basic update
Create `gedit ~/qmk/YtMusicDownloader/basic_update.sh`  
``` bash
#!/bin/sh

cp ~/qmk/YtMusicDownloader/src/ytMusicDownload.db ~/ytMusicDownload_bkp.db
cp ~/qmk/YtMusicDownloader/src/configuration.json ~/configuration_bkp.json
git -C ~/qmk/YtMusicDownloader pull
cp ~/ytMusicDownload_bkp.db ~/qmk/YtMusicDownloader/src/ytMusicDownload.db
cp ~/configuration_bkp.json ~/qmk/YtMusicDownloader/src/configuration.json
sudo docker restart qmk_ymd
```
Save and exit.  
Make the file executable: `sudo chmod +x ~/qmk/YtMusicDownloader/basic_update.sh`  
To run the script: `sudo ~/qmk/YtMusicDownloader/basic_update.sh`  
#### Full update
WARNING: this will erase your data!
Create `gedit ~/qmk/YtMusicDownloader/full_update.sh`  
``` bash
#!/bin/sh

git reset --hard
git -C ~/qmk/YtMusicDownloader pull
sudo docker container rm -f qmk_ymd
sudo docker build --no-cache -t qmk_yt_music_dl ~/qmk/YtMusicDownloader
sudo docker run -p 8092:8080 -v ~/qmk/YtMusicDownloader:/usr/src/app -v ~/Music:/Music -d --name qmk_ymd qmk_yt_music_dl
```
Don't forget to add your user_id in the `docker build` command!  
Save and exit.  
Make the file executable: `sudo chmod +x ~/qmk/YtMusicDownloader/full_update.sh`  
To run the script: `sudo ~/qmk/YtMusicDownloader/full_update.sh`  
### Create aliases
Create file `gedit ~/.bash_aliases` and insert the following:  
``` bash
# qmk software
alias ymd-st="sudo docker start qmk_ymd"  
alias ymd-sp="sudo docker stop qmk_ymd"  
alias ymd-bu="sudo ~/qmk/YtMusicDownloader/basic_update.sh"  
alias ymd-fu="sudo ~/qmk/YtMusicDownloader/full_update.sh"  
```
Apply your changes with `source ~/.bash_aliases`.  
### Create desktop launcher
Create file `sudo gedit /usr/share/applications/qmk_yt_music_downloader.desktop` and insert the following:  
``` bash
[Desktop Entry]  
Version = 1.0  
Type = Application  
Terminal = false  
Name = QMK YT Music Downloader  
Exec = sudo docker start qmk_ymd %f  
Icon = ~/qmk/YtMusicDownloader/icon.png  
Categories = Application;  
```
If you want to have a terminal open when running the app, remove the `%f` on the "Exec" line.  
For this launcher to work, it is required to make the system not ask for sudo password.  
Edit the file `sudo gedit /etc/sudoers` and add the following line at the end of the file:  
``` bash
qmk ALL=(ALL:ALL) NOPASSWD:/snap/bin/docker
```
*Note: you have to replace "qmk" with your own username.*  
Create an icon and rename/copy it to `~/qmk/YtMusicDownloader/icon.png`.  
Apply changes with `sudo update-desktop-database`.  
You could also create a stop or update launcher if you want. I mean, be creative, do whatever.   
### Make program run at startup
There are several ways to do this: use cron, use the "Startup Applications" program, etc.  
I'll let you google this if you want, I'm just laying this here as a suggestion.  
