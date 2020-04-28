from src.youtubedl import YoutubeDl


class Controller:
    @staticmethod
    def update_youtube_dl():
        print("update youtube-dl")
        return YoutubeDl.update().stdout
