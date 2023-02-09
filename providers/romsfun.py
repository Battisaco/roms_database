from typing import List

import requests
from bs4 import BeautifulSoup

import utils
from typings import Console, Game, Rom

url = "https://romsfun.com/roms"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}


def get_consoles() -> List[Console]:
    """Get all consoles from romsfun.com"""

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    consoles = soup.select(".row > div > a")

    list: List[Console] = []
    for console in consoles:
        footer = console.select("span.small > span")
        data: Console = {
            "provider": "romsfun",
            "url": str(console["href"]).strip(),
            "image": str(console.select("img")[0]["src"]).strip(),
            "name": str(console.select(".h5")[0].text).strip(),
            "games": utils.str_to_int(footer[0].text.split(" ")[0]),
            "downloads": utils.str_to_int(footer[2].text),
        }
        list.append(data)

    return list


def get_games_for_console(console: Console) -> List[Game]:
    """Get all games for a console from romsfun.com"""

    console_url = console["url"]
    r = requests.get(console_url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    last_page_url = str(soup.select(".pagination > li > a")[-1]["href"])
    page_count = int(last_page_url.split("/")[-1])

    list = get_games_in_page(soup)
    for page in range(1, page_count + 1):
        r = requests.get(f"{console_url}/page/{page}", headers=headers)
        soup = BeautifulSoup(r.content, "html5lib")
        list += get_games_in_page(soup)

    return list


def get_games_in_page(soup: BeautifulSoup) -> List[Game]:
    """Get all games in a page from romsfun.com"""

    games = soup.select(".row > div > a")
    list: List[Game] = []

    for game in games:
        footer = game.select("div > div")
        data: Game = {
            "provider": "romsfun",
            "url": str(game["href"]).strip(),
            "image": str(game.select("img")[0]["src"]).strip(),
            "name": str(game.select(".h5")[0].text).strip(),
            "rating": utils.str_to_float(footer[2].attrs["data-rateyo-rating"]),
            "downloads": utils.str_to_int(footer[0].text),
        }
        list.append(data)

    return list


def get_roms_for_game(game: Game) -> List[Rom]:
    """Get all roms for a game from romsfun.com"""

    game_url = game["url"]
    r = requests.get(game_url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    download_page_url = str(soup.select(".entry-content > a")[0]["href"])
    r = requests.get(download_page_url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    roms = soup.select("table > tbody > tr")

    list: List[Rom] = []
    for rom in roms:
        data: Rom = {
            "name": str(rom.select("td")[0].text).strip(),
            "size": str(rom.select("td")[1].text).strip(),
            "type": str(rom.select("td")[2].text).strip(),
            "url": str(rom.select("td > a")[0]["href"]).strip(),
        }
        list.append(data)

    return list
