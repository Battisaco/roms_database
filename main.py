import providers.romsfun


def run():
    consoles = providers.romsfun.get_consoles()
    games = providers.romsfun.get_games_for_console(consoles[0])
    roms = providers.romsfun.get_roms_for_game(games[0])

    print(roms)


if __name__ == "__main__":
    run()
