import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QGraphicsPixmapItem
import main



class MainWindow (QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(150, 50, 860, 700)
        self.home()
        self.setStyleSheet("background-color : ;")
        self.setWindowTitle("Sound To Motion - STM")

    def home(self):
        icon = QtGui.QIcon('rec4.png')
        but = QPushButton("Record", self) # Creates the brew coffee button
        but.setIcon(icon)
        but.clicked.connect(self.gif_display)
        but.resize(200, 80)
        but.move(50, 150)





        self.show()

    @QtCore.pyqtSlot()
    def gif_display(self):
        l = QMovieLabel(main.record(), self)
        l.move(300, 50)
        l.adjustSize()
        l.show()

class QMovieLabel(QLabel):
    def __init__(self, fileName, parent=None):
        super(QMovieLabel, self).__init__(parent)
        m = QtGui.QMovie(fileName)
        self.setMovie(m)
        m.start()

    def setMovie(self, movie):
        super(QMovieLabel, self).setMovie(movie)
        s=movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()

def run():
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()