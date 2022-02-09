import sys
from io import BytesIO

import requests
from PIL import Image
from PyQt5 import uic
from PyQt5.Qt import *


def get_toponym(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return toponym


def get_ll(address):
    toponym = get_toponym(address)

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])

    env = toponym['boundedBy']['Envelope']
    x1, y1 = env['lowerCorner'].split()
    x2, y2 = env['upperCorner'].split()
    dx = abs(float(x1) - float(x2)) / 2
    dy = abs(float(y1) - float(y2)) / 2
    span = f'{dx},{dy}'
    return ll, span


def get_picture(address, with_label=False):
    ll_span = get_ll(address)
    label = None
    if with_label:
        label = ll_span[0] + "," + "pm2rdl"

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ll_span[0], "spn": ll_span[1], "l": "map", "pt": label
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)

    # image = Image.open(BytesIO(response.content))
    image = Image.open(BytesIO(response.content))
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gg.ui', self)
        # address = " ".join(sys.argv[1:])
        address = "python3 main.py Moscow"
        if address:
            image = get_picture(address, with_label=True)
            self.label.setPixmap(QPixmap(image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = Main()
    ex1.show()
    sys.exit(app.exec_())