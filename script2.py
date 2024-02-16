import json
import requests


def put_data():
    # URL вашего DRF API для загрузки данных
    url = 'http://127.0.0.1:8000/upload/'

    # Если ваш API требует аутентификации, укажите здесь свой токен или данные для аутентификации
    token = 'acd04ef4aad1c36897b372f64bf37f268e05919c'
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    # Чтение данных из JSON-файла
    with open('all_data.json', 'r',encoding="utf-8") as file:
        data = json.load(file)
    response = requests.post(url, headers=headers, json=data)
    # Проверка статус-кода ответа
    if response.status_code == 201:
    # Если запрос успешен, выведите ответ на экран
        print('Данные успешно загружены.')
    else:
    # Если запрос неуспешен, выведите сообщение об ошибке
        print('Ошибка при загрузке данных: STATUS', response.status_code)
        print(response.text)

put_data()
