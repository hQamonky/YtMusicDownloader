from src.youtube_dl import YoutubeDl


class Controller:
    @staticmethod
    def update_youtube_dl():
        print("Updating youtube-dl...")
        return YoutubeDl.update()

    @staticmethod
    def list_playlist(playlist_id):
        # playlist_id = "PLCVGGn6GhhDu_4yn_9eN3xBYB4POkLBYT"
        result = YoutubeDl.list_playlist(YoutubeDl.playlist_url() + playlist_id)
        return result

    @staticmethod
    def get_video_info(video_id):
        # video_id = "2UcPJYZ_Ta0"
        result = YoutubeDl.get_video_info(YoutubeDl.video_url() + video_id)
        return result

    @staticmethod
    def download_music(video_id):
        video_id = "2UcPJYZ_Ta0"
        result = YoutubeDl.download_music(YoutubeDl.video_url() + video_id, "/.%(ext)s")
        return result
