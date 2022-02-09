import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image


def get_toponym(url):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": url,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return toponym


def get_ll(address):
    toponym = get_toponym(address)
    toponym_coodrinates = toponym["Point"]["pos"]
    ll = ",".join(toponym_coodrinates.split(" "))
    env = toponym['boundedBy']['Envelope']
    x1, y1 = env['lowerCorner'].split()
    x2, y2 = env['upperCorner'].split()
    dx = abs(float(x1) - float(x2)) / 2
    dy = abs(float(y1) - float(y2)) / 2
    span = f"{dx},{dy}"
    return ll, span

def get_toponym(url):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": url,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return toponym


def get_ll(address):
    toponym = get_toponym(address)
    toponym_coodrinates = toponym["Point"]["pos"]
    ll = ",".join(toponym_coodrinates.split(" "))
    env = toponym['boundedBy']['Envelope']
    x1, y1 = env['lowerCorner'].split()
    x2, y2 = env['upperCorner'].split()
    dx = abs(float(x1) - float(x2)) / 2
    dy = abs(float(y1) - float(y2)) / 2
    span = f"{dx},{dy}"
    return ll, span


def get_pic(url, with_label=False):
    ll_span = get_ll(url)
    label = None
    if with_label:
        label = ll_span[0] + "," + "flag"
    map_params = {
        "ll": ll_span[0],
        "spn": ll_span[1],
        "l": "map",
        "pt": label
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()

toponym_to_find = " ".join(sys.argv[1:])
get_pic(toponym_to_find, with_label=True)