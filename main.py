import sys

import requests
from PyQt5 import uic
from PyQt5.Qt import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gg.ui', self)
        self.coord = ''
        self.zoom1 = 0.0
        self.zoom2 = 0.0
        self.flag = True
        self.map_request = ''
        self.response = ''
        self.pushButton.clicked.connect(self.get_picture)
        self.map_file = "map.png"

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up and self.zoom1 < 25.0 and self.zoom2 < 25.0:
            self.zoom1 += 2
            self.zoom2 += 2
            self.get_picture()

        if event.key() == Qt.Key_Down and self.zoom1 > 2.0 and self.zoom2 > 2.0:
            self.zoom1 -= 2
            self.zoom2 -= 2
            self.get_picture()

    def get_picture(self):
        if self.flag:
            self.coord = self.lineEdit.text()
            self.zoom1 = float(self.lineEdit_4.text().split(',')[0])
            self.zoom2 = float(self.lineEdit_4.text().split(',')[1])
            self.flag = False
        self.map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.coord}&spn={self.zoom1},{self.zoom2}&l=sat"
        self.response = requests.get(self.map_request)
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)
        self.MAP.setPixmap(QPixmap(self.map_file))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = Main()
    ex1.show()
    sys.exit(app.exec_())
