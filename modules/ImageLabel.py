from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import tempfile

#This file hosts the image part of a video block. Originally shows the thumbail, 
#if a file is dropped on it, it will show the dropped image instead.

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.current_file_path = None

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setFixedSize(200, 200)
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')
        self.networkManager = QNetworkAccessManager()
        self.pixmap = QPixmap()  # Initialize pixmap

        self.setAcceptDrops(True)  # Enable drop events

    def setPixmapFromUrl(self, url):
        self.networkManager.finished.connect(self.onFinished)
        self.networkManager.get(QNetworkRequest(QUrl(url)))

    def onFinished(self, reply):
        data = reply.readAll()
        self.pixmap.loadFromData(data)
        self.updatePixmap()  # Update the pixmap when the image is loaded

    def updatePixmap(self):
        print("part 1")
        if not self.pixmap.isNull():  # Check if pixmap is not null
            # Scale pixmap to fit within a 200x200 square while maintaining aspect ratio
            self.scaled_pixmap = self.pixmap.scaled(
                200, 200,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(self.scaled_pixmap)
            print("part2")

            # Save the updated pixmap to disk
            self.save_photo_to_disk()

    def save_photo_to_disk(self):
        try:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            temp_file.close()

            # Save the pixmap to the temporary file
            self.pixmap.save(temp_file.name, "PNG")

            # Return the path to the temporary file
            self.current_file_path = temp_file.name
            print(self.current_file_path)
            return temp_file.name
        except Exception as e:
            print(f"An error occurred in save_photo_to_disk: {e}")
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.setPixmapFromUrl(url.toString())
            break  # Only handle the first dropped URL