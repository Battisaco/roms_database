import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
url = f"https://www.romsgames.net/roms/nintendo-ds/?letter=all&page=1&sort=popularity"
r = requests.get(url,headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
raw = str(soup.find_all('ul',class_='rg-gamelist'))
#print(raw.split('<li>')[1].find('href="')) ->31
#print(raw.split('<li>')[1].find('/">')) ->78
print(raw.split('<li>')[1][raw.split('<li>')[1].find('href="')+5
            :raw.split('<li>')[1].find('/">')+2])