from src.youtube_dl import YoutubeDl


class Controller:
    # Database management
    @staticmethod
    def get_playlists():
        return

    @staticmethod
    def create_playlist(json):
        return

    @staticmethod
    def get_playlists():
        return


    # Youtube-dl methods
    @staticmethod
    def update_youtube_dl():
        print("Updating youtube-dl...")
        return YoutubeDl.update()

    @staticmethod
    def list_playlist(playlist_id):
        result = YoutubeDl.list_playlist(YoutubeDl.playlist_url() + playlist_id)
        return result

    @staticmethod
    def get_video_info(video_id):
        result = YoutubeDl.get_video_info(YoutubeDl.video_url() + video_id)
        return result

    @staticmethod
    def download_music(video_id):
        result = YoutubeDl.download_music(YoutubeDl.video_url() + video_id, "./" + video_id + ".webm")
        return result
