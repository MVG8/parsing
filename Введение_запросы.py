import requests

# url = 'https://www.google.ru'
# #url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvDkXMQArUo1iHlTh4QL3uXU6TBvPBMIM6Rw&usqp=CAU'
# response = requests.get(url)
#
# if response.status_code == 200:
#     pass
# if response.ok:  # 200..399
#     pass
# response.raise_for_status()
#
# with open('file.html', 'wb') as f: # Вместо html jpg для скачивания картинки
#     f.write(response.content)
#
# print()

#Программа погоды
# import requests
#
# url = 'https://api.openweathermap.org/data/2.5/weather'
# city = 'Rostov-on-Don'
# appid = 'e5e4cd692a72b0b66ea0a6b80255d1c3'
#
# params = {'q': city,
#           'appid': appid}
#
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
#
# response = requests.get(url, params=params, headers=headers)
#
# j_data = response.json()
#
# print(f"В городе {j_data['name']} температура {j_data['main']['temp'] - 273.15} градусов")

#. (Обязательное) Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
# пользователя, сохранить JSON-вывод в файле *.json.
import requests
import json

url = 'https://api.github.com/users/octocat/repos'

response = requests.get(url)
for i in response.json():
    print(i['name'])

with open('data.json', 'w') as f:
    json.dump(response.json(), f)
#print(1)