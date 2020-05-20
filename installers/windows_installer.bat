REM Install chocolatey
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
call refreshenv
REM Install Docker
choco install -y docker-cli
REM Install git
choco install -y git.install
call refreshenv
REM Download project
if not exist "C:\ProgramData\qmk" mkdir "C:\ProgramData\qmk"
git -C "C:\ProgramData\qmk" clone https://github.com/hQamonky/YtMusicDownloader.git
REM Setup docker container
docker build --no-cache -t qmk_yt_music_dl "C:\ProgramData\qmk\YtMusicDownloader"
docker run -p 8092:8080 -v "C:\ProgramData\qmk\YtMusicDownloader":/usr/src/app -v %userprofile%\Music:/Music -d --name qmk_ymd qmk_yt_music_dl