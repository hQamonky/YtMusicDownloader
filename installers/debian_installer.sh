sudo apt update
# Install snapd
sudo apt install -y snapd
sudo service snapd start
# Install docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
sudo snap install docker
# Install git
sudo apt install -y  git
# Download project
mkdir ~/qmk
git -C ~/qmk clone https://github.com/hQamonky/YtMusicDownloader.git
# Setup docker container
sudo docker build --no-cache -t qmk_yt_music_dl ~/qmk/YtMusicDownloader
sudo docker run -p 8092:8080 -v ~/qmk/YtMusicDownloader:/usr/src/app -v ~/Music:/Music -d --name qmk_ymd qmk_yt_music_dl