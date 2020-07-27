import youtube_dl
import os


class YoutubeDownloader:
    def __init__(self):
        pass

    def __action(self, url, file_format, folder="/tmp", download=False):
        outtmpl = "/{}/%(title)s.%(ext)s".format(folder)
        if file_format == "mp3":
            opts = {
                "format": "bestaudio/best",
                "outtmpl": outtmpl,
                "postprocessors": [
                    {"key": "FFmpegExtractAudio",
                     "preferredcodec": "mp3",
                     "preferredquality": "192"},
                    {'key': 'FFmpegMetadata'},
                ],
            }
        else:
            opts = {
                "outtmpl": outtmpl,
                "format": file_format}
        downloader = youtube_dl.YoutubeDL(opts)
        with downloader:
            result = downloader.extract_info(url, download=download)

        return os.path.join(folder, "{}.{}".format(result["id"], result["ext"])), result

    def extract_info(self, url):
        return self.__action(url, download=False)

    def download(self, url, file_format, folder):
        return self.__action(url, file_format, folder, download=True)

    def validate(self):
        raise NotImplementedError


if __name__ == "__main__":
    some = YoutubeDownloader()
    file_ = some.extract_info("https://youtu.be/fmI_Ndrxy14")
