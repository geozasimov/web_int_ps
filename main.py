"""
This file contains all 
"""
import json
import requests
from jinja2 import Template
from dotenv import dotenv_values
 
MIEM_TOKEN = dotenv_values(".env").get("MIEM")
 
MIEM_PATH = "https://cabinet.miem.hse.ru/api/student_profile"
 
MIEM_HEADERS = {"x-auth-token": MIEM_TOKEN}
  
VK_TOKEN = dotenv_values(".env").get("VK")
 
PATH_VK = "https://api.vk.com/method/users.get"
 

ID_PROFILE_VK = "geozasimov"
 
FIELDS = "activities,about,books,bdate,can_write_private_message," \
    "career,connections,contacts,city," \
    "country,domain,education,followers_count,has_photo,has_mobile," \
    "home_town,photo_400_orig,sex,site,schools,screen_name,status," \
    "verified,games,interests,last_seen,maiden_name," \
    "military,movies,music,nickname,occupation,personal," \
    "quotes,relation,relatives,timezone,tv,universities"
 
vk_params = {"access_token": VK_TOKEN,
             "user_ids": ID_PROFILE_VK,
             "fields": FIELDS,
             "v": 5.131}
 
data_miem = requests.get(url=MIEM_PATH,
                         headers=MIEM_HEADERS,
                         timeout=10).json()
 
data_vk = requests.get(
    PATH_VK, params=vk_params, timeout=10).json()
 
"""
This is part of writing to json file.
"""
def write_to_json(data, json_name):
    """
    Writes in .json file information from the service.
    """
    with open(json_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
 
 
write_to_json(data_vk, 'data\\vk.json')
write_to_json(data_miem, 'data\\miem.json')
 
 
"""
This is part of creating html.
"""
def made_html_file():
    """
    Retrieves the received data from the services and returns them for html.
    """
    global data_miem, data_vk
    template = Template(open("rec/template.html", encoding='utf-8').read())
    return template.render(
        name = data_vk["response"][0]["first_name"],
        surname = data_vk["response"][0]["last_name"],
        #email = data_miem["data"][0]["main"]["email"],
        bdate = data_vk["response"][0]["bdate"],
        country = data_vk["response"][0]["country"]["title"],
        city = data_vk["response"][0]["city"]["title"],
        photo = data_vk["response"][0]["photo_400_orig"],
        #chat_link = data_miem["data"][0]["main"]["chatLink"],
        university = data_vk["response"][0]["occupation"]["name"],
        status = data_vk["response"][0]["status"]
    )
 
html = made_html_file()
with open("template.html", "w+", encoding='utf-8') as f:
    f.write(html)
