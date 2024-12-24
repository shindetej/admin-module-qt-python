from PySide6.QtWidgets import  QSplashScreen
from PySide6.QtGui import QPixmap,QMovie
from PySide6.QtCore import Qt
class CustomSplashScreen(QSplashScreen):
    def __init__(self, animation, flags):
        super().__init__(QPixmap(), flags)
        self.movie = QMovie(animation)
        self.movie.frameChanged.connect(self.onNextFrame)
        self.movie.start()

    def onNextFrame(self):
        pixmap = self.movie.currentPixmap()
        pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio)
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())