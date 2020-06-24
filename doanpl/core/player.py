import sys
import time

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSlider, QStyle, QVBoxLayout, QWidget,
                             QInputDialog, QProgressDialog,
                             QMainWindow, QAction)
from PyQt5.QtGui import QIcon
from .youtube_downloader import YoutubeDownloader


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
        url, ok = QInputDialog.getText(self, 'Download',
                                       'Insert youtube link: ')
        # TODO: Add url validation
        if ok:
            downloader = YoutubeDownloader()
            folder_name = QFileDialog.getExistingDirectory(self, 'Select Folder', "file:///" + QDir.currentPath())
            progress = QProgressDialog("Download video", "Cancel", 0, 0, self)
            progress.setMinimumDuration(0)
            progress.setRange(0, 100)
            progress.forceShow()
            downloader.download(url, folder_name)
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
