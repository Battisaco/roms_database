import os
import util
import test_util
 
def run():
    url = "https://romsfun.com/roms"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    consoles = util.get_consoles(url,headers)
    consoles_link = util.get_consoles_link(url,headers)

    util.create_console_table(consoles,consoles_link)

    util.console_loop(consoles_link,headers) 

    
if __name__ == "__main__":
    run()


'''
    game_link = ['https://romsfun.com/roms/game-boy/the-adventures-of-rocky-and-bullwinkle-and-friends.html',
                 'https://romsfun.com/roms/gamecube/shrek-extra-large.html',
                 'https://romsfun.com/roms/game-boy/the-legend-of-zelda-links-awakening.html',
                 'https://romsfun.com/roms/gamecube/fifa-street-6.html'] 

    temp = test_util.get_game_info_2(game_link[0],headers)
    print(temp)
    temp = test_util.get_game_info_2(game_link[1],headers)
    print(temp)
    temp = test_util.get_game_info_2(game_link[2],headers)
    print(temp)
    temp = test_util.get_game_info_2(game_link[3],headers)
    print(temp)
    

'''