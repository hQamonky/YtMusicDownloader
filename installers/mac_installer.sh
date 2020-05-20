# Install Docker
brew cask install docker; open /Applications/Docker.app
# Install Git
git --version
# Download project
mkdir ~/qmk
git -C ~/qmk clone https://github.com/hQamonky/YtMusicDownloader.git
# Setup docker container
sudo docker build --no-cache -t qmk_yt_music_dl ~/qmk/YtMusicDownloader
sudo docker run -p 8092:8080 -v ~/qmk/YtMusicDownloader:/usr/src/app -v ~/Music:/Music -d --name qmk_ymd qmk_yt_music_dl