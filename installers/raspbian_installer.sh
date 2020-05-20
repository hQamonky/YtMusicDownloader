sudo apt-get update
# Install docker
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo apt-get install -y libffi-dev libssl-dev
sudo apt-get install -y python3 python3-pip
sudo apt-get remove python-configparser
sudo pip3 install docker-compose
# Install git
sudo apt-get install -y  git
# Download project
mkdir ~/qmk
git -C ~/qmk clone https://github.com/hQamonky/YtMusicDownloader.git
# Setup docker container
sudo docker build --no-cache -t qmk_yt_music_dl ~/qmk/YtMusicDownloader
sudo docker run -p 8092:8080 -v ~/qmk/YtMusicDownloader:/usr/src/app -v ~/Music:/Music -d --name qmk_ymd qmk_yt_music_dl