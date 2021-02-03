import requests


def get_map_params(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
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
    
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    
    lowerCorner = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
    upperCorner = toponym["boundedBy"]["Envelope"]["upperCorner"].split()
    
    delta_x = str(float(upperCorner[0]) - float(lowerCorner[0]))
    
    # Собираем параметры для запроса к StaticMapsAPI:
    return {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta_x, delta_x]),
        "l": "map"
    }
