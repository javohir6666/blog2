import asyncio
import aiohttp
from bs4 import BeautifulSoup
from slugify import slugify
import json, requests
import unicodedata

url = 'https://sports.uz/news/view/aslonov-va-baturovda-galaba--abdullaev-esa-yutqazdi-10-02-2024'
base_url = 'https://sports.uz/'

relative_url = url.replace(base_url, 'https://sports.uz/oz/')
print(relative_url)