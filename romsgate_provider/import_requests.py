import requests
from bs4 import BeautifulSoup
  
url = "https://www.romsgames.net/roms/"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

r = requests.get(url,headers=headers)
  
soup = BeautifulSoup(r.content, 'html5lib') 
raw = str(soup.find_all('div', class_='thumbnailree')).split(',')

db_json = {}
for console in raw:
    temp = console.split('"')
    db_json[temp[3]]={}



