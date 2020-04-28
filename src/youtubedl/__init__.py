import subprocess


class YoutubeDl:
    @staticmethod
    def get_version():
        return subprocess.run(["youtube-dl", "--version"], check=True, stdout=subprocess.PIPE,
                              universal_newlines=True)

    @staticmethod
    def update():
        return subprocess.run(["youtube-dl", "--update"], check=True, stdout=subprocess.PIPE,
                              universal_newlines=True)
