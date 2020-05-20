# Install Docker
brew cask install docker; open /Applications/Docker.app
# Install Git
git --version
# Download project
mkdir /usr/local/bin/qmk
git -C /usr/local/bin/qmk clone https://github.com/hQamonky/YtMusicDownloader.git
# Setup docker container
sudo docker build --no-cache -t qmk_yt_music_dl /usr/local/bin/qmk/YtMusicDownloader
sudo docker run -p 8092:8080 -v /usr/local/bin/qmk/YtMusicDownloader:/usr/src/app -v ~/Music:/Music -d --name qmk_ymd qmk_yt_music_dl