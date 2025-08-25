import requests
import json
from bs4 import BeautifulSoup

json_list = []

for page in range(1000, 10000):
    print(page)
    response = requests.get(url=f"https://lukoil.bg/bg/ForMotorists/PetrolStation?type=gasStation&id={page}", headers={"Accept": "*/*", "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"})
    list_code = response.text
    main_soup = BeautifulSoup(list_code, 'lxml')
    check_str = main_soup.find('div', id='main')
    soup = BeautifulSoup(list_code, 'lxml')
    main = soup.find('div', id='main').get_text(strip=True)

    if 'Bulgaria' in main:

        soup = BeautifulSoup(list_code, 'lxml')
        main = soup.find('div', id='main')
        list_of_p = main.find_all("div", class_="row")
        for single_p in list_of_p:
            try:
                col_sm = single_p.find("div", class_='col-sm-9 col-md-9 content-block-left')
                name = col_sm.find("div", class_="row").find("div", class_="col-sm-12 col-md-12").find("div",
                                                                                                       id="wrapper-widLxtjNE5uVU6WSla1Dco4ug").find(
                    "div").find("div",
                                class_="panel-default panel-collapsible panel-contact-gas panel-contact-gas_station-gas").find(
                    "div", class_="panel-heading").find("h4").get_text(strip=True)
                address = col_sm.find("div", class_="row").find("div", class_="col-sm-12 col-md-12").find("div",
                                                                                                       id="wrapper-widLxtjNE5uVU6WSla1Dco4ug").find(
                    "div").find("div",
                                class_="panel-default panel-collapsible panel-contact-gas panel-contact-gas_station-gas").find(
                    "div", id="collapsable-div-6").find("div", class_="panel-body").find("div", class_="text").find("p").get_text(strip=True)[0:-12:]
                coordinates = col_sm.find("div", class_="row").find("div", class_="col-sm-12 col-md-12").find("div",
                                                                                                       id="wrapper-widLxtjNE5uVU6WSla1Dco4ug").find(
                    "div").find("div",
                                class_="panel-default panel-collapsible panel-contact-gas panel-contact-gas_station-gas").find(
                    "div", id="collapsable-div-6").find("div", class_="panel-body").find("div", id="collapsable-div-1").find("div", class_="user-coords").get_text()

                coordinate_N = float(coordinates[coordinates.index('N')+1:coordinates.index(' ')-1].replace(',', '.'))
                coordinate_E = float(coordinates[coordinates.index('E')+1:len(coordinates)].replace(',', '.'))


                mobile_phone = col_sm.find("div", class_="row").find("div", class_="col-sm-12 col-md-12").find("div",
                                                                                                       id="wrapper-widLxtjNE5uVU6WSla1Dco4ug").find(
                    "div").find("div",
                                class_="panel-default panel-collapsible panel-contact-gas panel-contact-gas_station-gas").find(
                    "div", id="collapsable-div-6").find("div", class_="panel-body").find("div", class_="text").find("div", class_="cells-wrap").find("div", class_='cell cell--contacts').find("div", class_="list-contacts").find("p").get_text(strip=True)


                fax_phone = col_sm.find("div", class_="row").find("div", class_="col-sm-12 col-md-12").find("div",
                                                                                                               id="wrapper-widLxtjNE5uVU6WSla1Dco4ug").find(
                    "div").find("div",
                                class_="panel-default panel-collapsible panel-contact-gas panel-contact-gas_station-gas").find(
                    "div", id="collapsable-div-6").find("div", class_="panel-body").find("div", class_="text").find(
                    "div", class_="cells-wrap").find("div", class_='cell cell--contacts').find_all("div",
                                                                                               class_="list-contacts")
                for inner_fax_phone in fax_phone:
                    if inner_fax_phone.find("i", class_='icon icon-s-fax') is not None:
                        res_fax = inner_fax_phone.get_text(strip=True)

                scripts = soup.find_all("script", type="text/javascript")
                non_stop_work = True
                for script in scripts:

                    if '"BusinessHours":[{"Days"' in script.get_text(strip=True):
                        limit_hours = script.get_text(strip=True)

                        non_stop_work = False
                    else:
                        pass
                if non_stop_work:
                    worktime = "mon - sun 00:00 - 24:00"

                    json_list.append({"name": name, 'address': address, 'location': [coordinate_N, coordinate_E], 'phones': [f"+359{mobile_phone.replace('/', '').replace(' ', '')}", f"+359{res_fax.replace('/', '').replace(' ', '')}"], 'working_hours': worktime})
                else:

                    json_list.append({"name": name, 'address': address, 'location': [coordinate_N, coordinate_E],
                                      'phones': [f"+359{mobile_phone.replace('/', '').replace(' ', '')}",
                                                 f"+359{res_fax.replace('/', '').replace(' ', '')}"],
                                      'working_hours': [f"{limit_hours[366:372].replace('ПН-НЕД', 'mon - sun')} {limit_hours[383:394].replace('–',' - ')}"]})

            except AttributeError:
                pass

with open('parsing_results.json', 'w') as file:
    json.dump(json_list, file, ensure_ascii=False, indent=2)












