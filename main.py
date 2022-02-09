import sys
from io import BytesIO

import requests
from PIL import Image
from PyQt5 import uic
from PyQt5.Qt import *


def get_picture():
    map_request = "http://static-maps.yandex.ru/1.x/?ll=133.693800,-25.794900&spn=15,15&l=sat"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gg.ui', self)
        image = get_picture()
        self.label.setPixmap(QPixmap(image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = Main()
    ex1.show()
    sys.exit(app.exec_())