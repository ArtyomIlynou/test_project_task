import requests
import json
from bs4 import BeautifulSoup

response = requests.get(url="https://n-l-e.ru/shops/", headers={"Accept": "*/*", "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"})
list_code = response.text

upper_list_of_json = []

soup = BeautifulSoup(list_code, "lxml")
main_div = soup.find("div", class_="shops")

list_of_shops = main_div.find("div", class_="shops__block_main")
shops_block_list = list_of_shops.find("div", class_="shops__block_list")
shops_id = shops_block_list.find("div", id="main_items")
first_items = shops_id.find("div", id="first_items")
section = first_items.find_all("div", class_="shops__white_box align_items_stretch shops__flexbox shops__list_item 9ddc37dc-1443-4d44-a4c9-96e658679522")

for element in section:
    city = element.find("p").find("a").get_text(strip=True)
    address = element.find("div", class_="shops__flexbox vertical_1440").find("div", class_="flexbox__column").find("p").find("span").get_text(strip=True)
    phone_number = element.find("div", class_="shops__flexbox vertical_1440").find("div", class_="flexbox__column").find_all("p")
    for number in phone_number:
        try:
            res_number = number.find("span", class_="icon icon_phone").get_text(strip=True)
        except AttributeError:
            pass
    worktime_div = element.find("div", class_="shops__flexbox vertical_1440").find_all("div", class_="flexbox__column")
    for worktime in worktime_div:
        try:
            res_worktime = worktime.find("p").find("span", class_="icon icon_clock").get_text(strip=True)
        except AttributeError:
            pass
    coordinates = element.find("div", class_= "shops__list_item__links").find_all("p")
    for coordinates_piece in coordinates:
        try:
            res_coordinates = coordinates_piece.find("a", class_="icon icon_map_route_google").get("href")
        except AttributeError:
            pass

    upper_list_of_json.append({"name": city, "address": address, "location": [float(res_coordinates[33:res_coordinates.index(',')]), float(res_coordinates[res_coordinates.index(',') + 1:-1])], "phones": [res_number], "working_hours": [str(res_worktime)]})

with open("task_1.json", "w", encoding='utf-8') as file:
    json.dump(upper_list_of_json, file, ensure_ascii=False, indent=2)
