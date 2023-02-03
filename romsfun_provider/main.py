

import os
import util

def run():
    url = "https://romsfun.com/roms"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    consoles = util.get_consoles(url,headers)
    consoles_link = util.get_consoles_link(url,headers)

    util.create_console_table(consoles,consoles_link)

    game_link = util.get_game_link(consoles_link[0],headers)

if __name__ == "__main__":
    run()
