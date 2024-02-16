import asyncio
import aiohttp
from bs4 import BeautifulSoup
from slugify import slugify
import json

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_section_data(session, section_url, category_id):
    # Base URL for constructing complete URLs
    base_url = "https://sports.uz"

    print(f"Fetching data from {section_url}...")

    html = await fetch(session, section_url)
    soup = BeautifulSoup(html, "html.parser")

    container = soup.select_one("#w0")
    products = container.find_all("div", class_="item")
    urls = [base_url + product.select_one("a")["href"].replace("../", "") for product in products]

    args = []
    for url in urls:
        url = url.replace(base_url, 'https://sports.uz/oz')
        print(f"Processing {url}...")

        html = await fetch(session, url)
        soup = BeautifulSoup(html, "html.parser")
        # Lotin alifbosiga o'tkazilgan matn
        title = soup.find('h1').text.strip()
        slug = slugify(title)

        body_all_p = soup.find('div', class_='news-body').find_all('p')
        if body_all_p:
            detail = body_all_p.pop()
        detail = ' '.join([p.text.strip() for p in body_all_p])

        view = 159
        img_url = soup.select_one("img.news-img").get("src")

        filename = img_url.split('/')[-1]
        async with session.get(img_url) as resp:
            with open(f'uploads/news-img/{filename}', 'wb') as f:
                f.write(await resp.read())
        img_path = f"news-img/{filename}"

        seo_keywords = soup.find('meta', attrs={'name': 'keywords'}).get('content')
        seo_description = soup.find('meta', attrs={'name': 'description'}).get('content')

        args.append({
            "title": title,
            "slug": slug,
            "image": img_path,
            "detail": detail,
            "category_id": category_id,
            "post_viewcount": view,
            "seo_keywords": seo_keywords,
            "seo_description": seo_description
        })

    return args

async def main():
    # List to store all data
    all_data = []

    # URLs and category IDs of different sections
    sections = {
        "https://sports.uz/oz/news/boxs": 1,
        "https://sports.uz/oz/news/football": 2,
        # Add more sections here as needed
    }

    async with aiohttp.ClientSession() as session:
        for section_url, category_id in sections.items():
            print(f"Scraping data for {section_url}...")
            data = await get_section_data(session, section_url, category_id)
            all_data.extend(data)

    # Save all data to a JSON file
    with open("all_data.json", "w", encoding="utf-8") as file:
        json.dump(all_data, file, indent=4, ensure_ascii=False)
    print("Data saved to all_data.json")

# Call the main function to start scraping
asyncio.run(main())
