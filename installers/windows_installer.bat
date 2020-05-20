REM Install chocolatey
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
REM Install Docker
choco install docker-cli
REM Install git
choco install git.install
REM Download project
if not exist "C:\Program Files\qmk" mkdir "C:\Program Files\qmk"
git -C "C:\Program Files\qmk" clone https://github.com/hQamonky/YtMusicDownloader.git
REM Setup docker container
docker build --no-cache -t qmk_yt_music_dl "C:\Program Files\qmk\YtMusicDownloader"
docker run -p 8092:8080 -v "C:\Program Files\qmk\YtMusicDownloader":/usr/src/app -v %userprofile%\Music:/Music -d --name qmk_ymd qmk_yt_music_dl