from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QMessageBox

from modules.VideoBlock import VideoBlock
from modules.StartWindow import StartWindow
from modules.Threads import ScraperThread

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1000, 850)  # Adjust the size of the main window
        self.VideosBlock_list = []
        self.initial_window_init()
        self.setWindowTitle('Youtube Playlist Downloader')
        
    def add_video_widget(self, metadata):
        if metadata[0] == 'FAILURE':
            if metadata[1] == 'HTTPError':
                error_dialog = QMessageBox()
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.setWindowTitle("HTTP Error")
                error_dialog.setText(f"An HTTP error occurred. You likely entered an invalid playlist URL.")

                error_dialog.exec_()
                QApplication.quit()  # Quit the appl
            if metadata[1] == 'URLError':
                error_dialog = QMessageBox()
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.setWindowTitle("URL Error")
                error_dialog.setText(f"An URL error occurred. You likely are not connected to the internet.")
                error_dialog.exec_()
                QApplication.quit()  # Quit the appl
            return
        
        self.VideosBlock_list.append(vb := VideoBlock(metadata, self))
        self.mainLayout.addWidget(vb)
        self.scrollArea.update()
        self.throbberLabel.hide()

    def switch_to_video_view(self):
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.mainLayout = QVBoxLayout()

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)

        scrollAreaWidget = QWidget()
        scrollAreaWidget.setLayout(self.mainLayout)
        scrollArea.setWidget(scrollAreaWidget)

        self.scrollArea = scrollArea
        self.layout().addWidget(scrollArea)
        
        url = self.ui.playlist_input.text() #get url from input box
        self.scraper_thread = ScraperThread(url) #pass url to scraper thread
        self.scraper_thread.signal.connect(self.add_video_widget) #connect signal to add_video_widget
       
        self.throbberLabel = QLabel(self)
        self.throbberLabel.setText('Loading...')
        self.mainLayout.addWidget(self.throbberLabel)

        # Center the throbber
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.throbberLabel)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.mainLayout.addLayout(vbox)   


       
        self.scraper_thread.start() #start thread


    
    def closeEvent(self, event):
        # Override closeEvent to ensure the thread stops when the application is closed
        if hasattr(self, 'scraper_thread') and self.scraper_thread.isRunning():
            self.scraper_thread.quit()  # Quit the thread
            self.scraper_thread.wait()  # Wait for the thread to finish
    
    def playlist_submission(self): #on click of submit button
        t = self.ui.playlist_input.text()
        if ('playlist' in t and (
            self.ui.playlist_input.text() != 'playlist')):
            print('valid playlist url')
            self.switch_to_video_view()
        if ('playlist' not in t and (
            'list' in t)):
            #extract playlist id from url
            t = t.split('&')
            #get the element that contains the playlist id
            for i in t:
                if 'list' in i: #list=somecode
                    t = f"https://www.youtube.com/playlist?{i}" #https://www.youtube.com/playlist?list=somecode
                    break
            self.ui.playlist_input.setText(t)
            self.switch_to_video_view()
        else:
            self.ui.label.setText('Invalid playlist url. Try again.')

        
    

    def initUI(self):
        mainLayout = QVBoxLayout()  # Use QVBoxLayout to arrange widgets vertically
        
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)  # Allow the scroll area to resize its contents
        scrollArea.setWidget(QWidget())  # Create a widget to contain the layout
        scrollArea.widget().setLayout(mainLayout)  # Set the layout inside the scroll area's widget

        mainLayoutContainer = QVBoxLayout(self)
        mainLayoutContainer.addWidget(scrollArea)

        self.mainLayoutForVideos = mainLayout


    def initial_window_init(self):
        self.mainLayout = QVBoxLayout()  
        self.uiWidget = QWidget()
        self.ui = StartWindow()
        self.ui.setupUi(self.uiWidget, self)
        self.mainLayout.addWidget(self.uiWidget)

        self.setLayout(self.mainLayout)


import sys

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('files/icon.png'))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())