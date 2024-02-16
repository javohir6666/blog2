import requests
from bs4 import BeautifulSoup
import datetime, json
from slugify import slugify

def get_box_data():
    url = "https://sports.uz/oz/news/boxs"

    base_url = "https://sports.uz"

    response = requests.get(url)

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    container = soup.select_one("#w0")

    products = container.find_all("div", {"class":"item"})

    urls = []
    for product in products:
        url = product.select_one("a")["href"]
        urls.append(base_url +url.replace("../", ""))
    args = []
    for url in urls:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find('h1').text.strip()
        slug = slugify(title)
        body_all_p = soup.find('div', class_='news-body').find_all('p')
        if body_all_p:
            detail = body_all_p.pop()
        detail = ' '.join([p.text.strip() for p in body_all_p])
        view = 159
        category = 1
        img_codes = soup.select_one("img.news-img").get("src")
        def save_img(img_codes):
            filename = img_codes.split('/')[-1]
            print(filename)
            r = requests.get(img_codes, allow_redirects=True)
            open(('uploads/news-img/')+filename,"wb").write(r.content)
        save_img(img_codes)
        file = img_codes.split('/')[-1]
        file_url = file.replace(file, f"news-img/"+file)
        seo_keywords = soup.find('meta', attrs={'name': 'keywords'}).get('content')
        seo_description = soup.find('meta', attrs={'name': 'description'}).get('content')
        args.append({"title":title,
                     "slug":slug,
                    "image":file_url, 
                    "detail":detail,
                    "category_id":category, 
                    "post_viewcount":view, 
                    "seo_keywords":seo_keywords, 
                    "seo_description":seo_description})
    with open("box.json", "w", encoding="utf-8") as file:
        json.dump(args, file, indent=4, ensure_ascii=False)
    
    

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
    # Чтение данных из JSON-файла
    with open('box.json', 'r',encoding="utf-8") as file:
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

def main():
    get_box_data()
    put_data()


if __name__ == "__main__":
    main()