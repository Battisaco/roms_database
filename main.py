import providers.romsfun
import providers.romsgames
from typings import Console,Rom,Game
import utils
import re
import time

import numpy as np
import pandas as pd

import json

providers = [providers.romsgames,
             providers.romsfun
             ]#

def update_console_name(console):
    # update console name using lookup table
    pass

def loas_DB(base):
    if base == "roms":
        f = open("Data/roms.json",)
        return json.load(f)
    
    elif base == "console":
        f = open("Data/console.json",)
        return json.load(f)
    
    elif base == "games":
        f = open("Data/games.json",)
        return json.load(f)
    
    else:
        print("No base loaded, returning new list")
        return []

def check_console_in_DB(json,console):
    '''
    receive the intire json representing the that saved and the current console 
        that could be saved, and than confirm that's new or already saved
    '''
    for console_b in json:
        if console_b["name"] == console['name']:
            print(f' found {console_b["name"]} ==> {console["name"]}')
            return console_b
    
    return False

def check_game_in_DB(json,game):
    '''
    receive the intire json representing the that saved and the current game 
        that could be saved, and than confirm that's new or already saved
    '''
    for game_b in json:
        if game_b["console_id"] == game["console_id"]:
            if list(game["url"].keys())[0] not in list(game_b["url"].keys()):
                aux_base = re.sub('[^A-Za-z0-9]+', '', game_b["name"]) #adjusting the string of the game in base
                aux_game = re.sub('[^A-Za-z0-9]+', '', game['name']) #adjusting the string of the game that it's checking
        
                point = utils.similar(aux_base,aux_game) #getting the similarity value, can sometimes failed to get a good score
                if (point > 0.85) or (aux_base == aux_game):
                    #print(f' found {game_b["name"]} ==> {game["name"]}')
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

def check_provider(name):
    if name == "romsgames":
        return providers[0]
    elif name == "romnfun":
        return providers[1]
    else:
        print("Provider not find")
        return None


def step_1():
    '''
    Get the consoles and games of the providers
    
    '''

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
                    print(f'updating {game["name"]}')
                    game["id"] = existing_game["id"]
                    update_game(games_json, game)

                else:
                    games_json.append(game)
            
    with open("Data/console.json", "w") as element:
        json.dump(consoles_json, element,indent=2)   

    with open("Data/games.json", "w") as element:
        json.dump(games_json, element,indent=2) 

def step_2():
    '''
    Get the roms of the consoles 
    '''
    roms_json: list[Rom]  = loas_DB("roms")

    game_base: list[Game] = loas_DB("games")

    #There is a chance that on the middle of the roms get, it stop 
    #to avoid time loss, when the program stops it will save
    start_time = time.time()
    print('Starting')
    try:
        for game_num in range(45819,len(game_base)):
            actual_game = game_base[game_num]
            if game_num%500==0:
                #A feedback on how the programs is going
                print()
                print(f'{np.round((game_num/(len(game_base)))*100,2)}%')
                print(f"{np.round((time.time() - start_time)/60,2)} Minutes")
                print(f"{np.round((time.time() - start_time)/3600,2)} Hours")
                time.sleep(3)


        #print(actual_game['url'])
            for site in actual_game['url']:
                #print(site,actual_game['url'][site])
                provider = check_provider(site)
                rom = provider.get_roms_for_game(actual_game,site)
                roms_json = roms_json + rom

    except:
        with open("Data/roms.json", "w") as element:    
            json.dump(roms_json, element,indent=2) 
        print(game_num,len(roms_json))         

    with open("Data/roms.json", "w") as element:
        json.dump(roms_json, element,indent=2)  

def run():
    #step_1()
    step_2()

if __name__ == "__main__":
    run()
