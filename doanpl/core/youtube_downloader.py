import youtube_dl
import os

class YoutubeDownloader:
    def __init__(self):
        pass

    def __action(self, url, folder="/tmp", download=False):
        downloader = youtube_dl.YoutubeDL({'outtmpl': '/{}/%(id)s.%(ext)s'.format(folder),
                                           'format': "mp4"})
        with downloader:
            result = downloader.extract_info(url, download=download)

        return os.path.join(folder, "{}.{}".format(result["id"], result["ext"])), result

    def extract_info(self, url):
        return self.__action(url, download=False)

    def download(self, url, folder):
        return self.__action(url, folder, download=True)

    def validate(self):
        raise NotImplemented

if __name__ == "__main__":
    some = YoutubeDownloader()
    file_ = some.extract_info("https://youtu.be/fmI_Ndrxy14")

    import pdb;pdb.set_trace()
