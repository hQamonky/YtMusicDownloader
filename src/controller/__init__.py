from src.youtube_dl import YoutubeDl


class Controller:
    @staticmethod
    def update_youtube_dl():
        print("Updating youtube-dl...")
        return YoutubeDl.update()

    @staticmethod
    def list_playlist():
        result = YoutubeDl.list_playlist("https://www.youtube.com/playlist?list=PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT")
        return result
