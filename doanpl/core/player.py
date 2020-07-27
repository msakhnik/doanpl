import sys
import time
import pyperclip as pc

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSlider, QStyle, QVBoxLayout, QWidget,
                             QInputDialog, QProgressDialog,
                             QMainWindow, QAction, QDialog, QDialogButtonBox,
                             QButtonGroup, QRadioButton
                             )
from PyQt5.QtGui import QIcon
from .youtube_downloader import YoutubeDownloader


class DownloadingDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(DownloadingDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Insert Youtube Link!")
        self.dialog_label = QLabel("Link: ")
        self.link_text_edit = QLineEdit()
        url = pc.paste()
        # TODO: add regexp to check youtube url
        if "youtu" in url:
            self.link_text_edit.setText(url)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.h_layout_url = QHBoxLayout()
        self.h_layout_url.addWidget(self.dialog_label)
        self.h_layout_url.addWidget(self.link_text_edit)

        self.letter_group = QButtonGroup(self)
        self.mp3 = QRadioButton("MP3")
        self.letter_group.addButton(self.mp3)
        self.mp4 = QRadioButton("MP4")
        self.mp4.setChecked(True)
        self.letter_group.addButton(self.mp4)
        self.h_layout_format = QHBoxLayout()
        self.h_layout_format.addWidget(self.mp3)
        self.h_layout_format.addWidget(self.mp4)

        self.layout.addLayout(self.h_layout_url)
        self.layout.addLayout(self.h_layout_format)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        self.play_button = QPushButton()
        self.back_button = QPushButton()
        self.main_widget = QWidget(self)
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_timer = QLabel()

        self.__init_menu_bar()
        self.__init_control_elements()
        self.__init_layouts()
        self.__init_media_player()

    def __init_menu_bar(self):
        open_action = QAction(QIcon(), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open)

        exit_action = QAction(QIcon(), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.exit_call)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

        download_action = QAction(QIcon(), '&Download from Youtube', self)
        download_action.setShortcut('Ctrl+D')
        download_action.triggered.connect(self.download)
        tools_menu = menu_bar.addMenu('&Tools')
        tools_menu.addAction(download_action)

    def __init_control_elements(self):
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play)
        self.play_button.setShortcut("space")
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(lambda x: self.media_player.setPosition(x))

    def __init_layouts(self):
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)

        control_layout = QHBoxLayout()
        control_layout.addLayout(button_layout)
        control_layout.addWidget(self.position_slider)
        control_layout.addWidget(self.position_timer)

        # TODO: QSplitter
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addLayout(control_layout)

        self.main_widget.setLayout(layout)
        self.setCentralWidget(self.main_widget)

    def __init_media_player(self):
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(lambda x: self.position_slider.setValue(x))
        self.media_player.durationChanged.connect(lambda x: self.position_slider.setRange(0, x))
        self.media_player.positionChanged.connect(lambda x: self.position_timer.setText(
            "{} -> {}".format(time.strftime('%M:%S', time.gmtime(x // 1000)),
                              time.strftime('%M:%S', time.gmtime(self.media_player.duration() // 1000)))))

    def open(self):
        # TODO: remove abs path
        file_, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                               "/home/morwin/Videos/")
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_)))
        self.play_button.setEnabled(True)
        self.play()

    def download(self):
        dlg = DownloadingDialog(self)
        if dlg.exec_():
            downloader = YoutubeDownloader()
            folder_name = QFileDialog.getExistingDirectory(self, 'Select Folder', "file:///" + QDir.currentPath())
            progress = QProgressDialog("Download video", "Cancel", 0, 0, self)
            progress.setMinimumDuration(0)
            progress.setRange(0, 100)
            progress.forceShow()
            # TODO: change the simple logic to add more formats
            file_format = "mp4" if dlg.mp4.isChecked() else "mp3"
            print(file_format)
            downloader.download(dlg.link_text_edit.text(), file_format, folder_name)
            progress.close()

    def exit_call(self):
        sys.exit(app.exec_())

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def media_state_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
