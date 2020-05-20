REM Download project
if not exist "C:\Program Files\qmk" mkdir "C:\Program Files\qmk"
git -C "C:\Program Files\qmk" clone https://github.com/hQamonky/YtMusicDownloader.git
REM Setup docker container
docker build --no-cache -t qmk_yt_music_dl "C:\Program Files\qmk\YtMusicDownloader"
docker run -p 8092:8080 -v "C:\Program Files\qmk\YtMusicDownloader":/usr/src/app -v %userprofile%\Music:/Music -d --name qmk_ymd qmk_yt_music_dl