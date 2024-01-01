from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox #for error popup

from modules.YoutubeInterface import Scraper

#These are the threads that are used in the program to prevent the UI from freezing
#during downloads. The ScraperThread is used to scrape the playlist metadata video by video
#and the DownloadThread is used to trigger the individual download of videos.

class ScraperThread(QThread):
    signal = pyqtSignal(tuple)

    def __init__(self, urls):
        QThread.__init__(self)
        self.urls = urls

    def run(self):
        scraper = Scraper()
        s = scraper.get_urls_simple(self.urls)

        
        for metadata in scraper.get_information_simul(s):
            if not metadata[0]:
                self.signal.emit(("FAILURE",metadata[1]))
                break
            self.signal.emit(metadata)
            QApplication.processEvents() 
        

        self.quit()  # Quit the thread

class DownloadThread(QThread):
    def __init__(self, video):
        QThread.__init__(self)
        self.video = video

    def run(self):
        self.video.download_video()