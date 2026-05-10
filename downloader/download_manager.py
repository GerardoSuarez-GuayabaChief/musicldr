import yt_dlp
import os


class DownloadManager:

    def __init__(self, progress_callback=None, status_callback=None):

        self.progress_callback = progress_callback
        self.status_callback = status_callback

    def download_song(self, song, output_path):

        def progress_hook(d):

            if d['status'] == 'downloading':

                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 1)

                percent = downloaded / total

                if self.progress_callback:
                    self.progress_callback(percent)

                speed = d.get('speed', 0)

                if speed:
                    speed_mb = speed / 1024 / 1024

                    if self.status_callback:
                        self.status_callback(
                            f"Descargando... {percent:.0%} | {speed_mb:.2f} MB/s"
                        )

            elif d['status'] == 'finished':

                if self.status_callback:
                    self.status_callback("Convirtiendo a MP3...")

        ydl_opts = {
            'format': 'bestaudio/best',

            'outtmpl': os.path.join(
                output_path,
                '%(title)s.%(ext)s'
            ),

            'progress_hooks': [progress_hook],

            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],

            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            ydl.download([song['url']])

        if self.progress_callback:
            self.progress_callback(1)

        if self.status_callback:
            self.status_callback("Descarga completada !")