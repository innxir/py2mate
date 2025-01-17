import os
import subprocess
import dotenv
from yt_dlp import YoutubeDL

class Video:
    def __init__(self, url: str):
        self.path = f"..\\output\\video\\"
        self.url = url
        self.ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True
        }
        self.video_info = self.getVideo(self.url)
        self.name = self.video_info.get('title')

    def getVideo(self, url: str):
        # print(f"\033[5mConnecting to {url}\033[0m")
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print("\033[92mConnection established\033[0m\n")
            print(f"\033[93;1mVideo Info\033[0m:\nVideo title: \033[95m{info.get('title')}\033[0m; Video id: \033[95m{info.get('id')}\033[0m, \nVideo from: \033[95m{info.get('extractor')}\033[0m, Uploader: \033[95m{info.get('uploader')}\033[0m\n")
            return info

    def download(self, path=None):
        if path is None:
            path = self.path
        print(f"Downloading video titled \033[95m\"{self.name}\"\033[0m to \033[100;3m{path}\033[0m\n")
        download_opts = dict(self.ydl_opts)
        download_opts['outtmpl'] = f'{path}/%(title)s.%(ext)s'
        with YoutubeDL(download_opts) as ydl:
            ydl.download([self.url])
        print(f"Downloaded \033[95m\"{self.name}\033[0m to \033[100;3m{path}\033[0m\n")


class Converter:
    def __init__(self, video:Video, path=None):
        self.video = video
        self.name = video.name
        self.path = f"..\\output\\audio"
        self.videopath = os.path.join(video.path, f"{video.name}.mp4")
        if path is not None:
            self.path = path

    def convert(self):
        output_path = os.path.join(self.path, f"{self.name}.mp3")
        print(f"Converting \033[95m\"{self.name}\"\033[0m\n")

        try:
            command = [
                'ffmpeg',
                '-i', self.videopath,
                '-vn',  # No video
                '-acodec', 'libmp3lame',
                '-ab', '192k',
                '-ar', '44100',  # Sample rate
                '-y',  # Overwrite output file
                output_path
            ]
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"Error during conversion: {stderr.decode()}\n")
                return False

            if dotenv.dotenv_values().get('DELETE_VIDEOS') == "True":
                os.remove(self.videopath)
            return True
        
        except Exception as e:
            print(f"An error occurred: {str(e)}\n")
            return False
