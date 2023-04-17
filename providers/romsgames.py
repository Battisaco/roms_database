from typing import List
import numpy as np
import pandas as pd
import time
import uuid

import requests
from bs4 import BeautifulSoup

import utils
from typings import Console, Game, Rom

url = "https://www.romsgames.net"
url_rom = "https://www.romsgames.net/roms/"
headers = {'User-Agent': utils.random_header()}

def get_provider() -> str:
    return 'romsgames'


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
            "id": str(uuid.uuid4()),
            "name": str(console.select("img")[0]["alt"]).strip().lower(),
            "image":str(console.select("img")[0]["src"]).strip().lower(),
            "url": {'romsgames':(url + str(console["href"]).strip()).lower()}
        }
        list.append(data)

    return list

def get_games_for_console(console: Console) -> List[Game]:
    """Get all games for a console from romsgames.com"""
    
    list_g :List[Game] = [] 

    console_url = list(console["url"].values())[0]
    headers = {'User-Agent': utils.random_header()}
    r = requests.get(console_url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    page_count = len(soup.select(".pagination li+ li a"))
    
    list_g += get_games_in_page(soup,console)
    print(f'Console:{console["name"]}, 0%')

    for page in range(2, page_count +1):
        if page%5==0:
            print(f'Console:{console["name"]},' \
                    f'{np.round((page/(page_count +1))*100,2)}%')
            time.sleep(1)
        headers = {'User-Agent': utils.random_header()}
        r = requests.get(f"{console_url}?page={page}", 
                            headers=headers)
        soup = BeautifulSoup(r.content, "html5lib")
        list_g += get_games_in_page(soup,console)


    return list_g       



def get_games_in_page(soup: BeautifulSoup,console) -> List[Game]:
    """Get all games in a page from romsgames.com"""
    games = soup.select(".rg-gamelist a")
    list: list[Game] = []

    for game in games:
        data: Game = {
            "id": str(uuid.uuid4()),
            "console_id":console["id"],
            "name": str(game.select("img")[0]["alt"]).strip().lower(),
            "image": str(game.select("img")[0]["src"]).strip().lower(),
            "console": console["name"],
            "url": {'romsgames':url + str(game['href']).strip().lower()}
        }
        list.append(data)

        #rating and release will get from another place
    
    return list

def get_roms_for_game_old(game: Game) -> List[Rom]:
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
        
        if flag%1000==0:
            time.sleep(5)
            print('milestone, sleep for 5 seconds') 

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

def get_roms_for_game(game: Game, site: str) -> List[Rom]:
    """Get all roms for a game from romsgames.com"""
    list: List[Rom] = []

    game_url = game["url"][site]
    headers = {'User-Agent': utils.random_header()}
    r = requests.get(game_url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    try:
        name     = soup.select(".rom-title")[0].text.strip()
    except:
        name     = None
        print(f'Problem in {game_url}')
    
    #try:
        #rom_url  = soup.select(".w-100")
        #url + soup.select("form")[1]["action"].strip()
    #except:
        #rom_url  = None
        #print(f'Problem in {game_url}')
    
    try:
        size     = soup.select(".gameinfo li+ li")[0].text.strip()
        version  = soup.select(f"div.rg-gamebox-info > ul.gameinfo" \
                                "> li > img")[0]["alt"].strip()
    except:
        size     =None
        version  =None

    data: Rom = {
            "id": str(uuid.uuid4()),
            "game_id": game["id"],
            "name": name,
            "size": size,
            "type": ".zip",
            "link":game_url,
            "provider":site,
            "version": version,
        }
    list.append(data)
        
    return list


def test():
    print("ok")