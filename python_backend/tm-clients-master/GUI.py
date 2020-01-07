import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QGraphicsPixmapItem, QVBoxLayout
import main
import threading
import time




class Application(QtCore.QObject):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)


class MainWindow (QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.move(150, 50)
        self.setFixedSize(850, 600)
        self.screen()
        self.setStyleSheet("background-color : ;")
        self.setWindowTitle("Dźwięk na Ruch - DnR")



    def screen(self):

        #Przycisk "Nagrywanie"
        icon = QtGui.QIcon('ui/icons/rec5.png')
        self.button = QPushButton("Nagrywanie", self)
        self.button.setIcon(icon)
        self.button.clicked.connect(self.gif_display)
        self.button.resize(200, 80)
        self.button.move(50, 230)

        #Wyświetlacz gifów
        self.gif_holder1 = QMovieLabel("ui/animations/waiting.gif", self)
        self.gif_holder1.move(450, 200)
        self.gif_holder1.adjustSize()
        self.gif_holder1.hide()
        self.gif_holder = QMovieLabel("ui/animations/DnR.gif", self)
        self.gif_holder.move(300, 15)
        self.gif_holder.adjustSize()




        #Podpis słowo klucz
        font = QtGui.QFont('Mono', 10)
        font.setBold(True)
        self.keyword = QLabel("Proszę rozpocząć nagrywanie", self)
        self.keyword.setFixedWidth(500)
        self.keyword.setAlignment(QtCore.Qt.AlignCenter)
        self.keyword.move(300, 550)
        self.keyword.setFont(font)

        #Notyfikacja o przesterze (światełko)
        self.green_led_off = 'ui/icons/green_led_off'
        self.green_led_on = 'ui/icons/green_led_on'
        self.red_led_on = 'ui/icons/red_led_on'
        self.led = QLabel(self)
        self.led.setFixedHeight(50)
        self.led.setFixedWidth(50)
        self.led.setPixmap(QtGui.QPixmap(self.green_led_off))
        self.led.move(125, 350)

        #Notyfikacja o przesterze (podpis)
        font1 = QtGui.QFont('Mono', 5)
        font1.setBold(True)
        self.peak_text = QLabel(self)
        self.peak_text.setWordWrap(True)
        self.peak_text.setAlignment(QtCore.Qt.AlignCenter)
        self.peak_text.setFixedWidth(250)
        self.peak_text.move(30, 425)
        self.peak_text.setFont(font)

        #Baner
        font2 = QtGui.QFont('Mono', 50)
        font2.setBold(True)
        self.banner = QLabel("DnR", self)
        self.banner.setFixedWidth(200)
        self.banner.setFixedHeight(200)
        self.banner.setAlignment(QtCore.Qt.AlignCenter)
        self.banner.move(50, 5)
        self.banner.setFont(font2)



        self.show()



    def loading_animation(self):
        self.gif_holder.hide()
        self.gif_holder1.show()
        self.peak_text.setText("Trwa nagrywanie...")
        self.led.setPixmap(QtGui.QPixmap(self.green_led_on))
        self.keyword.setText("Proszę mówić")


    def recording(self):

        self.gif_holder1.hide()
        self.gif_holder.hide()
        mazzny_condition = main.record()

        if mazzny_condition is True:
            self.gif_holder = QMovieLabel("ui/animations/err.gif", self)
            self.gif_holder.move(300, 15)
            self.gif_holder.adjustSize()
            self.gif_holder.show()
            self.led.setPixmap(QtGui.QPixmap(self.red_led_on))
            self.keyword.setText("Doszło do przesterowania sygnału!")
            self.peak_text.setText("Proszę mówić ciszej lub odsunąć się od mikorofonu i spróbować ponownie")
        else:
            key_phrase = main.classify()
            self.gif_holder = QMovieLabel('gifs/' + key_phrase + '.gif', self)
            self.gif_holder.move(300, 15)
            self.gif_holder.adjustSize()
            self.gif_holder.show()
            self.keyword.setText(key_phrase)
            self.led.setPixmap(QtGui.QPixmap(self.green_led_on))
            self.peak_text.setText("Rozpoznano frazę")

    @QtCore.pyqtSlot()
    def gif_display(self):
        #self.loading_animation()
        #self.button.setDisabled(True)
        self.recording()
        #self.button.setDisabled(False)

class QMovieLabel(QLabel):
    def __init__(self, fileName, parent=None):
        super(QMovieLabel, self).__init__(parent)
        m = QtGui.QMovie(fileName)
        self.setMovie(m)
        m.start()

    def setMovie(self, movie):
        super(QMovieLabel, self).setMovie(movie)
        s = movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()




def run():
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
