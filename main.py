import sys
from io import BytesIO

import requests
from PIL import Image
from PyQt5 import uic
from PyQt5.Qt import *



class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gg.ui', self)
        self.initUI()

    
    def initUI(self):
        self.pushButton.clicked.connect(self.get_picture)

    def get_picture(self):
        self.map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.lineEdit.text()}&spn={self.lineEdit_4.text()}&l=sat"
        print(self.map_request)
        self.response = requests.get(self.map_request)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)
        self.MAP.setPixmap(QPixmap(self.map_file))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = Main()
    ex1.show()
    sys.exit(app.exec_())