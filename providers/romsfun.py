from typing import List
import numpy as np
import time
import uuid

import requests
from bs4 import BeautifulSoup

import utils
from typings import Console, Game, Rom

url = "https://romsfun.com/roms"


def get_consoles() -> List[Console]:
    """
    Get all consoles from romsfun.com
    """
    headers = {"User-Agent": utils.random_header()}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    consoles = soup.select(".row > div > a")

    list: List[Console] = []
    for console in consoles:
        footer = console.select("span.small > span")
        data: Console = {
            "id": str(uuid.uuid4()),
            "name": str(console.select(".h5")[0].text).strip(),
            "image": str(console.select("img")[0]["src"]).strip(),
            "url": {"romsfun": str(console["href"]).strip()},
        }
        list.append(data)

    return list


def get_games_for_console(console: Console) -> List[Game]:
    """Get all games for a console from romsfun.com"""

    list_g: List[Game] = []

    console_url = list(console["url"].values())[0]
    headers = {"User-Agent": utils.random_header()}
    r = requests.get(console_url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    last_page_url = str(soup.select(".pagination > li > a")[-1]["href"])
    page_count = int(last_page_url.split("/")[-1])

    list_g += get_games_in_page(soup, console)
    print(f'Console:{console["name"]}, 0%')

    for page in range(2, page_count + 1):
        if page % 5 == 0:
            print(
                f'Console:{console["name"]},'
                f"{np.round((page/(page_count +1))*100,2)}%"
            )
            time.sleep(1)
        headers = {"User-Agent": utils.random_header()}
        r = requests.get(f"{console_url}/page/{page}", headers=headers)
        soup = BeautifulSoup(r.content, "html5lib")
        list_g += get_games_in_page(soup, console)

    return list_g


def get_games_in_page(soup: BeautifulSoup, console) -> List[Game]:
    """Get all games in a page from romsfun.com"""

    games = soup.select(".row > div > a")
    list: List[Game] = []

    for game in games:
        try:
            name = str(game.select(".h5")[0].text).strip()
        except:
            name = None

        try:
            image = str(game.select("img")[0]["src"]).strip()
        except:
            image = None

        data: Game = {
            "id": str(uuid.uuid4()),
            "console_id": console["id"],
            "name": name,
            "image": image,
            "console": console["name"],
            "url": {"romsfun": str(game["href"]).strip()},
        }
        list.append(data)

    return list


def get_roms_for_game(game: Game, site: str) -> List[Rom]:
    """Get all roms for a game from romsfun.com"""

    game_url = game["url"][site]
    headers = {"User-Agent": utils.random_header()}
    r = requests.get(game_url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    try:
        download_page_url = str(soup.select(".entry-content > a")[0]["href"])
    except:
        return []

    r = requests.get(download_page_url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    roms = soup.select("table > tbody > tr")

    list: List[Rom] = []
    for rom in roms:
        try:
            name = str(game.select(".h5")[0].text).strip()
            version = name.split(" ")[-1]
        except:
            name = None
            version = None

        try:
            size = str(rom.select("td")[1].text).strip()
        except:
            size = None

        try:
            type = str(rom.select("td")[2].text).strip()
        except:
            type = None

        try:
            url = str(rom.select("td > a")[0]["href"]).strip()
        except:
            url = None

        data: Rom = {
            "id": str(uuid.uuid4()),
            "game_id": game["id"],
            "name": name,
            "size": size,
            "type": type,
            "provider": site,
            "url": url,
            "version": version,
        }
        list.append(data)

    return list
