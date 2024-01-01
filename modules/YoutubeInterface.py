from yt_dlp import YoutubeDL
from pytube import Playlist

import os

from urllib.error import HTTPError, URLError

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox #for error popup

import eyed3

class DownloadThread(QThread):
    def __init__(self, ydl, url):
        QThread.__init__(self)
        self.ydl = ydl
        self.url = url

    def run(self):
        self.ydl.download([self.url])


class Scraper:
    
    def __init__(self, url=None):
        self.url = url
    
    #UNUSED
    def get_playlist_urls(self,  url =None):
        urls = []

        ydl = YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet':False,'no_warnings':False})
        video = url

        with ydl:
            result = ydl.extract_info \
            (video,
            download=False) #We just want to extract the info

            if 'entries' in result:
                # Can be a playlist or a list of videos
                video = result['entries']

                #loops entries to grab each video_url
                for i, item in enumerate(video):
                    video = result['entries'][i]
                    video_url = video['webpage_url']
                    urls.append(video_url)

            return urls

    def get_urls_simple(self, url):
        return Playlist(url).video_urls #insanely fast, compared to get_playlist_urls
    
    #UNUSED
    def get_urls(self, url): #the workaround for the blocking issue caused by yt-dlp
        i = 1
        while True:
            ydl_opts = {
                'getid': True,
                'skip_download': True,
                'playlist_items': str(i),
                'quiet': True,
                'no_warnings': True
            }
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                try:
                    yield f"https://www.youtube.com/watch?v={info_dict['entries'][0]['id']}"
                except IndexError:
                    break

            i += 1

    def get_information_simul(self, urls : list[str]) -> list[tuple[str, str, str, str, int]]: #returns list of tuples
        with ThreadPoolExecutor() as executor:
            try:
                futures = {executor.submit(self.get_information, url) for url in urls}
                for future in as_completed(futures):
                    yield future.result() #allows metadata to be retrieved individually
            except HTTPError as e:
                print(e)
                yield (False, 'HTTPError')
            except URLError as e:
                yield (False, 'URLError')


    def get_information(self, url=None):
        if url is None:
            url = self.url
        with YoutubeDL({'quiet': False}) as ydl:
            metadata = ydl.extract_info(url, download=False)

        thumbnail = metadata['thumbnail']
        title = metadata['title'] 
        uploader = metadata['uploader'] #channel name
        upload_date = metadata['upload_date'] #YYYYMMDD
        length = metadata['duration'] #seconds

        return thumbnail, title, uploader, upload_date, length, url
    
    def download_video(self, url, 
        title, artist, album, image_path, video_metadata_view): #called in VideosView by the Download button
        
        title = title.replace("/", "／") #to allow for slashes without adding directories
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'./Downloads/{title}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }

        # with YoutubeDL(ydl_opts) as ydl:
        #     video_metadata_view.change_download_button_text('Downloading...')
        #     ydl.download([url])

        with YoutubeDL(ydl_opts) as ydl:
            video_metadata_view.change_download_button_text('Downloading...')
            download_thread = DownloadThread(ydl, url)
            download_thread.start()

        while download_thread.isRunning():
            QApplication.processEvents()

        

        video_metadata_view.change_download_button_text('Saving...')
        print(a := os.path.abspath(f"./Downloads/{title}.mp3"))
        audiofile = eyed3.load(a)
        if audiofile.tag is None:
            audiofile.initTag(2, 3, 0)
        audiofile.title = title
        audiofile.tag.artist = artist
        audiofile.tag.images.set(3, open(image_path,'rb').read(), 'image/png', u"cover")
        audiofile.tag.album = album
        
        audiofile.tag.save()

        video_metadata_view.change_download_button_text('Done!')
        import time
        time.sleep(1)
        video_metadata_view.change_download_button_text('Download Again')

        

        

        

        

        



class Downloader:
    def __init__(self, playlist_url):
        self.options = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        self.url = playlist_url

   