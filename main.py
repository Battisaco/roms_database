import providers.romsfun
import providers.romsgames

def run():
    #consoles = providers.romsfun.get_consoles()
    #games = providers.romsfun.get_games_for_console(consoles[0])
    #roms = providers.romsfun.get_roms_for_game(games[0])

    consoles = providers.romsgames.get_consoles()
    games = providers.romsgames.get_games_for_console(consoles[0])
    print(games)


if __name__ == "__main__":
    run()
