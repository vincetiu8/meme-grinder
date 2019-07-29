import requests
import shutil
from bs4 import BeautifulSoup

url = 'https://www.reddit.com/r/memes/'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
headers = {'User-Agent': user_agent}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')
for a in soup.find_all('a'):
    if a.img:
        print(a.img['src'])
        url = a.img['src']
        response = requests.get(url, stream=True)
        with open('img.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
