import random
import re
from difflib import SequenceMatcher

import jellyfish


def similar(a, b):
    # sim = jellyfish.damerau_levenshtein_distance(a, b)
    sim = SequenceMatcher(None, a, b).ratio()
    return sim


def str_to_int(s: str) -> int:
    """Converts a string to an integer."""
    return int(s.strip().replace(",", ""))


def str_to_float(s: str) -> float:
    """Converts a string to a float."""
    return float(s.strip())


def random_header():
    """
    Get a random header for every consult, in this way avoid getting the
    ip banned
    """
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36",
    ]
    user_agent = random.choice(user_agent_list)

    return user_agent


def update_console_name(str):
    name = {
        "game boy (gb)": "gameboy",
        "game boy color": "gameboy color",
        "gba": "gameboy advance",
        "nes": "super nintendo",
        "playstation (ps)": "playstation",
        "ps2": "playstation 2",
        "ps3": "playstation 3",
        "ps4": "playstation 4",
        "psp": "playstation portable",
        "sega dreamcast": "dreamcast",
        "snes": "super nintendo",
        "wii u": "nintendo wii u",
        "xbox": "microsoft xbox",
        "xbox 360": "microsoft xbox 360",
    }
    temp = str.lower()
    if temp in name.keys():
        str = name[str.lower()]

    return str.lower()


def check_game_name(series, str):
    """
    Function to check if a game is already on tha base
    """

    for game in series:
        game = re.sub("[^A-Za-z0-9]+", "", game)
        str = re.sub("[^A-Za-z0-9]+", "", str)
        point = similar(game, str)

        if (point > 0.85) or (game == str):
            """The game is problaby already in DB"""
            return 0

    return 1
