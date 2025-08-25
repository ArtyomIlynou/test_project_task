import requests
import json
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

import random

json_base_list = []
response = requests.get(url="https://ufahimchistka.ru/reception/", headers={"Accept": "*/*", "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"})
list_code = response.text
main_soup = BeautifulSoup(list_code, 'lxml')
section = main_soup.find("div", class_="row row-cols-1 row-cols-md-4")
list_of_pieces = section.find_all("div", class_="col mb-4")
for piece in list_of_pieces:
    address = piece.find("div", class_="card-header").get_text(strip=True)
    name = piece.find("p")

    str_of_info = str(name).replace('<p class="card-text">', '').replace('</p>', '').replace('<br/>', ' , ')
    list_of_info = str_of_info.split(sep=' , ')
    name_of_place = list_of_info[0]
    mobile_phone = f"+7(347){list_of_info[1]}"
    if 'Ремонт одежды' in list_of_info[2:5]:
        worktime = list_of_info[2:5]
        worktime.remove('Ремонт одежды')

    else:
        worktime = list_of_info[2:5]

    geolocator = Nominatim(user_agent=f'origik{random.randrange(16,1000)}')
    geo_address = address
    if "." in address:
        location = geolocator.geocode(f"{address[address.index('.')+1:len(address)]}, Уфа")

    else:
        location = geolocator.geocode(f"{address}, Уфа")

    if location:
        latitude = location.latitude
        longitude = location.longitude

        json_base_list.append({"name": name_of_place, 'address': address, 'location': [location.latitude, location.longitude], "phones": [mobile_phone], 'working_hours': worktime})

    else:
        print(f"Не удалось найти координаты для адреса: {address}")


with open("task_2.json", "w", encoding='utf-8') as file:
    json.dump(json_base_list, file, ensure_ascii=False, indent=2)

