#Generated from PyQt5 UI

#This file hosts the metadata part of a video block.
from PyQt5 import QtCore, QtGui, QtWidgets

class VideoMetadataView(object):
    def __init__(self, metadata):
        metadata = [str(i) for i in metadata]
        self.m_thumbnail = metadata[0]
        self.m_title = metadata[1]
        self.m_uploader = metadata[2]
        self.m_length = metadata[4]
        self.m_url = metadata[5]

    def setupUi(self, Form, ParentVideoBlock):
        self.ParentVideoBlock = ParentVideoBlock
        Form.setObjectName("Form")
        Form.resize(700, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.title = QtWidgets.QLineEdit(Form)
        self.title.setGeometry(QtCore.QRect(0, 0, 701, 91))
        self.title.setStyleSheet("background-color: rgba(0,0,0,0);")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(25)
        self.title.setFont(font)
        self.title.setStyleSheet("border: 3px solid black;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName(self.m_title)
        self.uploader = QtWidgets.QLineEdit(Form)
        self.uploader.setGeometry(QtCore.QRect(10, 100, 330, 30))
        self.uploader.setStyleSheet("background-color: rgba(0,0,0,0);")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.uploader.setFont(font)
        self.uploader.setObjectName(self.m_uploader)
        self.album = QtWidgets.QLineEdit(Form)
        self.album.setGeometry(QtCore.QRect(360, 100, 330, 30))
        self.album.setStyleSheet("background-color: rgba(0,0,0,0);")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.album.setFont(font)
        self.album.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.album.setObjectName("Unnamed Album")
        
        self.time = QtWidgets.QLabel(Form)
        self.time.setGeometry(QtCore.QRect(656, 68, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.time.setFont(font)
        self.time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time.setObjectName("time")

        self.download = QtWidgets.QPushButton(Form)
        self.download.setGeometry(QtCore.QRect(534, 136, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.download.setFont(font) 
        self.download.setObjectName("download")
        self.download.clicked.connect(lambda: ParentVideoBlock.download_video(original = True))  

        self.apply_artist = QtWidgets.QPushButton(Form)
        self.apply_artist.setGeometry(QtCore.QRect(179, 149, 171, 32))
        self.apply_artist.setObjectName("change_artist")
        self.apply_artist.clicked.connect(lambda: ParentVideoBlock.apply_artist_to_video())
        
        self.apply_cover = QtWidgets.QPushButton(Form)
        self.apply_cover.setGeometry(QtCore.QRect(14, 149, 171, 32))
        self.apply_cover.setObjectName("change_title")
        self.apply_cover.clicked.connect(lambda: ParentVideoBlock.apply_image_to_video())

        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(5, 3, 87, 20))
        self.checkBox.setObjectName("checkBox")

        self.apply_album = QtWidgets.QPushButton(Form)
        self.apply_album.setGeometry(QtCore.QRect(342, 149, 181, 32))
        self.apply_album.setObjectName("apply_album")
        self.apply_album.clicked.connect(lambda: ParentVideoBlock.apply_album_to_video())

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def if_checked(self):
        return self.checkBox.isChecked()

    
    def change_download_button_text(self, text):
        self.download.setText(text)
        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.title.setText(_translate("Form", self.m_title))
        self.uploader.setText(_translate("Form", self.m_uploader))
        self.album.setText(_translate("Form", 'Unnamed Album'))
        self.time.setText(_translate("Form", self.m_length))
        self.download.setText(_translate("Form", "Download"))
        self.checkBox.setText(_translate("Form", "Download"))
        self.apply_cover.setText(_translate("Form", "Apply Cover to Selected"))
        self.apply_artist.setText(_translate("Form", "Apply Artist to Selected"))
        self.apply_album.setText(_translate("Form", "Apply Album to Selected"))



