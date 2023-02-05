import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import test_util

def get_consoles(url,headers):

    r = requests.get(url,headers=headers)
    
    soup = BeautifulSoup(r.content, 'html5lib') 
    raw = soup.select('.mt-3')

    console_list = []
    for console in raw:
        temp = str(console).split('\n')
        console_list.append(temp[1])

    return console_list

def get_consoles_link(url,headers):

    r = requests.get(url,headers=headers)
    
    soup = BeautifulSoup(r.content, 'html5lib')
    raw = str(soup.find_all('a', class_="text-center bg-white border rounded shadow-sm d-flex flex-column h-100 p-3")) 
    
    indexes = [m.start() for m in re.finditer('href=', raw)]
    console_link = []
    
    for index in indexes:
        temp = raw[index+6:index+200].split('"')
        console_link.append(temp[0])

    return console_link

def get_game_link(console_link,headers):
    game_link = []
    lastpage = False
    page = 1
    print(console_link)
    while(lastpage == False):

        r = requests.get(console_link+f'/page/{page}',headers=headers)
        
        soup = BeautifulSoup(r.content, 'html5lib')
        raw = str(soup.find_all('a', class_="text-center bg-white border rounded shadow-sm d-flex flex-column h-100 p-3")) 
        indexes = [m.start() for m in re.finditer('href=', raw)]
        
        if len(indexes)<1:
            print('ĹastPage, moving to next console')
            print('----------------')
            print()
            return game_link
        
        for index in indexes:
            temp = raw[index+6:index+200].split('"')
            game_link.append(temp[0])
        page+=1
    return game_link



def create_game_table(game_link,headers):
    

    for aux_game_link in game_link:
        df = pd.DataFrame(columns=['name', 'console', 
                        'genre','region','publisher',
                        'views','download','released','rate',
                        'site','link'])
        count = 1
        flag = True
        for link in aux_game_link:

            table = {}
            
            info = test_util.get_game_info(link,headers)
            print(f'Jogo {count} de {len(aux_game_link)}')
            
            if flag == True:
                console_name = info[2]
                if console_name != 'None':
                    flag = False
            count+=1

            table['name']      = info[0]
            table['rate']      = info[1]
            table['console']   = info[2]
            table['publisher'] = info[3]
            table['genre']     = ','.join(info[4])
            table['region']    = info[5]
            table['views']     = info[6]
            table['download']  = info[7]
            table['released']  = info[8]
            
            table['site'] = 'ROMSFUN.com'
            table['link'] = link

            temp = pd.DataFrame(table, index=[0])
            df = pd.concat([df,temp], ignore_index=True)
        df.to_csv(os.path.join(os.path.dirname(__file__), f'game_tables/games_table_{console_name}.csv'),index=False)
        
def create_console_table(console,console_link):
    temp = {'Console':console,
            'Link':console_link,
            'site':'ROMSFUN.com'}

    df = pd.DataFrame(temp)
    df.to_csv(os.path.join(os.path.dirname(__file__), 'Console_table.csv'),index=False)

def console_loop(console_link,headers):
    game_links = []
    for aux_console_link in console_link:
        print(f'Start get game_link for {aux_console_link}')
        game_links.append(get_game_link(aux_console_link,headers))

    create_game_table(game_links,headers)