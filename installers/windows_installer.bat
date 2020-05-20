REM Download project
if not exist %userprofile%\qmk mkdir %userprofile%\qmk
git -C %userprofile%\qmk clone https://github.com/hQamonky/YtMusicDownloader.git
REM Setup docker container
docker build --no-cache -t qmk_yt_music_dl ~/qmk/YtMusicDownloader
docker run -p 8092:8080 -v %userprofile%/qmk/YtMusicDownloader:/usr/src/app -v %userprofile%/Music:/Music -d --name qmk_ymd qmk_yt_music_dl