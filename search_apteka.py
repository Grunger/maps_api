import os
import sys
import pygame
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
from pprint import pprint

import requests
from PIL import Image, ImageDraw
from geo import get_map_params

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

map_params = get_map_params(toponym_to_find)

address_ll = map_params["ll"]

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "caf9d482-85c9-4643-a5ca-733c627c05d0"
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz",
    "results": "1"
}
response = requests.get(search_api_server, params=search_params)
pprint(response.content.decode())
json_response = response.json()
organization = json_response["features"][0]
point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
map_params["pt"] = f"{org_point},pm2dgl~{address_ll},pm2ntl"
map_params.pop("spn")
map_params.pop("ll")
# ... и выполняем запрос
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
text = 'Адрес: '


pygame.init()

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
font = pygame.font.Font(None, 20)
text = 'Адрес:'
text_screen = font.render(text, True, (100, 50, 255))
screen.blit(text_screen, (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
