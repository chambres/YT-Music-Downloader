from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import tempfile

#local classes
from modules.VideoMetadataView import VideoMetadataView
from modules.ImageLabel import ImageLabel
from modules.YoutubeInterface import Scraper
from modules.Threads import DownloadThread


class VideoBlock(QWidget):
    def __init__(self, metadata, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.metadata = metadata
        self.resize(950, 400)  # Adjust the size of the main window
        self.setAcceptDrops(True)

        mainLayout = QHBoxLayout()  # Use QHBoxLayout to arrange widgets horizontally

        self.photoViewer = ImageLabel()
        self.photoViewer.setPixmapFromUrl(self.metadata[0])
        self.photoViewer.setFixedSize(200, 200)  # Keeps the image from resizing the window
        mainLayout.addWidget(self.photoViewer, alignment=Qt.AlignTop)

        #import .ui widget here
        self.uiWidget = QWidget()
        self.ui = VideoMetadataView(self.metadata)
        self.ui.setupUi(self.uiWidget, self)
        mainLayout.addWidget(self.uiWidget)

        self.setLayout(mainLayout)

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))
        self.photoViewer.save_photo_to_disk()

    def apply_image_to_video(self):
        for video in self.MainWindow.VideosBlock_list:
            if video.ui.checkBox.isChecked():
                tmp_pixmap = QPixmap(self.photoViewer.current_file_path)
                scaled_pixmap = tmp_pixmap.scaled(
                    200, 200,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                video.photoViewer.setPixmap(scaled_pixmap)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                temp_file.close()
                #Save the pixmap to the temporary file
                scaled_pixmap.save(temp_file.name, "PNG")
                video.photoViewer.current_file_path = temp_file.name

    def apply_artist_to_video(self):
        for video in self.MainWindow.VideosBlock_list:
            if video.ui.checkBox.isChecked():
                video.ui.uploader.setText(self.ui.uploader.text())

    def apply_album_to_video(self):
        for video in self.MainWindow.VideosBlock_list:
            if video.ui.checkBox.isChecked():
                video.ui.album.setText(self.ui.album.text())



    def download_video(self, original=False):
        c = 0
        if original and self.ui.checkBox.isChecked():
            self.download_threads = []
            for video in self.MainWindow.VideosBlock_list:
                if video.ui.checkBox.isChecked():
                    c+=1
                    download_thread = DownloadThread(video)
                    download_thread.start()
                    self.download_threads.append(download_thread)
            if c > 0:
                return

        Scraper().download_video(
            self.metadata[5], #url
            self.ui.title.text(),
            self.ui.uploader.text(), #artist
            self.ui.album.text(),
            self.photoViewer.current_file_path,
            self.ui
        )


    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Get the dropped data
        data = event.mimeData()
        urls = data.urls()

        if urls and urls[0].isLocalFile():
            # Load the image into a QPixmap
            image_path = str(urls[0].toLocalFile())
            self.pixmap = QPixmap(image_path)

            # Scale the image to fit in the label
            self.scaled_pixmap = self.pixmap.scaled(
                200, 200, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )

            # Update the widget that displays the QPixmap
            self.photoViewer.setPixmap(self.scaled_pixmap)

        

    def set_image(self, file_path):
        self.pixmap = QPixmap(file_path)
        self.scaled_pixmap = self.pixmap.scaled(
            200, 200, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.photoViewer.setPixmap(self.scaled_pixmap)