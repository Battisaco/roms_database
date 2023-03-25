import providers.romsfun
import providers.romsgames
from typings import Console,Rom,Game
import utils
import re

import pandas as pd

import json

providers = [providers.romsgames,
             providers.romsfun
             ]#

def update_console_name(console):
    # update console name using lookup table
    pass

def check_console_in_DB(json,console):
    for console_b in json:
        if console_b["name"] == console['name']:
            print(f' found {console_b["name"]} ==> {console["name"]}')
            return console_b
    
    return False

def check_game_in_DB(json,game):
    for game_b in json:
        if game_b["console_id"] == game["console_id"]:
            if list(game["url"].keys())[0] not in list(game_b["url"].keys()):
                aux_base = re.sub('[^A-Za-z0-9]+', '', game_b["name"])
                aux_game = re.sub('[^A-Za-z0-9]+', '', game['name'])
                point = utils.similar(aux_base,aux_game)
                if (point > 0.85) or (aux_base == aux_game):
                    print(f' found {game_b["name"]} ==> {game["name"]}')
                    return game_b
    
    return False

def update_console(json,console):
    for id,console_b in enumerate(json):
        if console_b["id"] == console["id"]:
            json[id]["url"].update(console["url"])

    return json

def update_game(json,game):
    for id,game_b in enumerate(json):
        if game_b["id"] == game["id"]:
            json[id]["url"].update(game["url"])

    return json


def step_1():

    consoles_json: list[Console] = []
    games_json: list[Game]       = []

    for provider in providers:

        consoles: list[Console] = provider.get_consoles()

        for console in consoles:
            
            #normalize and update name
            console["name"] = utils.update_console_name(console["name"])

            # upsert console in consoles_json
            existing_console = check_console_in_DB(consoles_json, console)

            if existing_console:
                console["id"] = existing_console["id"]
                consoles_json = update_console(consoles_json, console)
            else:
                consoles_json.append(console)
        
            # get games for console
            games = provider.get_games_for_console(console)

            for game in games:

                # upsert game in games_json
                # should match game by name and console
                existing_game = check_game_in_DB(games_json, game)

                if existing_game:
                    game["id"] = existing_game["id"]
                    update_game(games_json, game)

                else:
                    games_json.append(game)
            

    with open("Data/console_v2.json", "w") as element:
        json.dump(consoles_json, element,indent=2)   

    with open("Data/game_v2.json", "w") as element:
        json.dump(games_json, element,indent=2) 

def run():
    step_1()

if __name__ == "__main__":
    run()
