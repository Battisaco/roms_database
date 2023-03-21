from typing import List
import numpy as np

import requests
from bs4 import BeautifulSoup

import utils
from typings import Console, Game, Rom

url = "https://www.romsgames.net"
url_rom = "https://www.romsgames.net/roms/"
headers = {'User-Agent': utils.random_header()}

def get_consoles() -> List[Console]:
    '''
    Get all consoles from romsgames.com
    '''
    headers = {'User-Agent': utils.random_header()}
    r = requests.get(url_rom,headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    consoles = soup.select(".rg-consolelist a")

    list: List[Console] = []
    for console in consoles:
        data: Console = {
            "name": str(console.select("img")[0]["alt"]).strip().lower(),
            "image":str(console.select("img")[0]["src"]).strip().lower(),
            "temp_url": ("https://www.romsgames.net" + 
                         str(console["href"]).strip()).lower(),
        }
        list.append(data)

    return list

def get_games_for_console(console: Console) -> List[Game]:
    """Get all games for a console from romsgames.com"""
    
    list = []
    for console_dict in console:

        console_url = console_dict["temp_url"]
        headers = {'User-Agent': utils.random_header()}
        r = requests.get(console_url, headers=headers)
        soup = BeautifulSoup(r.content, "html5lib")

        page_count = len(soup.select(".pagination li+ li a"))
        
        list += get_games_in_page(soup,console_dict["name"])
        print(f'Console:{console_dict["name"]}, 0%')

        for page in range(2, page_count +1):
            if page%5==0:
                print(f'Console:{console_dict["name"]},' \
                      '{np.round((page/(page_count +1))*100,2)}%')
            headers = {'User-Agent': utils.random_header()}
            r = requests.get(f"{console_url}?page={page}", 
                             headers=headers)
            soup = BeautifulSoup(r.content, "html5lib")
            list += get_games_in_page(soup,console_dict["name"])

    return list       



def get_games_in_page(soup: BeautifulSoup,console_name) -> List[Game]:
    """Get all games in a page from romsgames.com"""
    games = soup.select(".rg-gamelist a")
    list: list[Game] = []

    for game in games:
        data: Game = {
            "name": str(game.select("img")[0]["alt"]).strip().lower(),
            "image": str(game.select("img")[0]["src"]).strip().lower(),
            "console": console_name,
            "temp_url":url + str(game['href']).strip().lower(),
        }
        #rating and release will get from another place
    
    return list

def get_roms_for_game(game: Game) -> List[Rom]:
    """Get all roms for a game from romsgames.com"""
    list: List[Rom] = []
    Console_name = 'start'
    flag = 1
    for game_dict in game:

        if game_dict['console'] != Console_name:
            Console_name = game_dict['console']
            print(f'Starting to get {Console_name} roms')           

        if flag%100==0:
            print(f'We are in {np.round((100*flag/len(game)),2)}%') 

        game_url = game_dict["temp_url"]
        headers = {'User-Agent': utils.random_header()}
        r = requests.get(game_url, headers=headers)
        soup = BeautifulSoup(r.content, "html5lib")

        try:
            name     = soup.select(".rom-title")[0].text.strip()
        except:
            name     = None
            print(f'Problem in {game_url}')
        
        try:
            rom_url  = url + soup.select("form")[1]["action"].strip()
        except:
            rom_url  = None
            print(f'Problem in {game_url}')
        
        try:
            size     = soup.select(".gameinfo li+ li")[0].text.strip()
            version  = soup.select(f"div.rg-gamebox-info > ul.gameinfo" \
                                    "> li > img")[0]["alt"].strip()
        except:
            size     =None
            version  =None

        data: Rom = {
                "name": name,
                "size": size,
                "type": ".zip",
                "provider":"romsgames.com",
                "url": rom_url,
                "version": version,
            }
        list.append(data)

        flag+=1
        
    return list