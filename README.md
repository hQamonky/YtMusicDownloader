# YtMusicDownloader
YtMusicDownloader is a python service that downloads music from YouTube automatically. Service is manageable through an integrated API.  
YtMusicDownloader uses youtube-dl to download files. Shout-outs to them and [here](https://github.com/ytdl-org/youtube-dl)'s the project page.
## Installation
You can run the service with Docker. Youtube-dl is integrated in the docker container.
### Docker
1. Build the docker container  
`sudo docker-compose build --no-cache`
2. Run the container  
`sudo docker-compose up`
