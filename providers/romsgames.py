from typing import List

import requests
from bs4 import BeautifulSoup

import utils
from typings import Console, Game, Rom

url = "https://www.romsgames.net/roms/"
headers = {'User-Agent': utils.random_header()}

def get_consoles() -> List[Console]:
    '''
    Get all consoles from romsgames.com
    '''

    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    consoles = soup.select(".rg-consolelist a")

    list: List[Console] = []
    for console in consoles:
        data: Console = {
            "provider":"romsgames",
            "url": ("https://www.romsgames.net" + str(console["href"]).strip()).lower(),
            "name":str(console.select("img")[0]["src"]).strip().lower(),
            "image": str(console.select("img")[0]["alt"]).strip().lower(),
        }
        list.append(data)

    return list

def get_games_for_console(console: Console) -> List[Game]:
    """Get all games for a console from romsgames.com"""

    console_url = console["url"]
    r = requests.get(console_url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    pags_num = len(soup.select(".pagination li+ li a"))
    
    list = get_games_in_page(soup,console_url)


def get_games_in_page(soup: BeautifulSoup,console_url) -> List[Game]:
    """Get all games in a page from romsgames.com"""
    games = soup.select(".rg-gamelist a")
    list: list[Game] = []

    for game in games:
        provider = "romsgames"
        url = console_url[:-1] + str(game['href']).strip().lower()
        image = str(game.select("img")[0]["src"]).strip().lower()
        name = str(game.select("img")[0]["alt"]).strip().lower()


        #rating,,downloads,release
        print(name)

