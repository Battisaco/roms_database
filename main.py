import providers.romsfun
import providers.romsgames

import json

def run():
    create_base_data()
    #add_too_base_data('/Data')

def create_base_data():
    """The Base data is from the romsgames provider"""
    
    '''
    consoles = providers.romsgames.get_consoles()

    with open("Data/consoles.json", "w") as final_I:
        json.dump(consoles, final_I,indent=2)
    
    games = providers.romsgames.get_games_for_console(consoles[50:])

    with open("Data/games.json", "w") as final_II:
        json.dump(games, final_II,indent=2)   

    roms_list = providers.romsgames.get_roms_for_game(games[60000:])

    test = roms + roms_list
    with open("Data/roms.json", "w") as final_III:
       json.dump(test, final_III,indent=2)  
    '''
    pass

def load_base_data():

    consoles = open("Data/consoles.json")
    consoles = json.load(consoles)

    games = open("Data/games.json")
    games = json.load(games)

    roms = open("Data/roms.json")
    roms = json.load(roms)

    return consoles,games,roms


def add_too_base_data(**kwargs):
    #consoles = providers.romsfun.get_consoles()
    #games = providers.romsfun.get_games_for_console(consoles[0])
    #roms = providers.romsfun.get_roms_for_game(games[0])
    pass

if __name__ == "__main__":
    run()
