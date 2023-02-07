import requests
from bs4 import BeautifulSoup
import random
import re
import pandas as pd
import os
import util


def romsgames_request():
    '''
    First function, call all the others in the main
    '''
    path = os.path.dirname(__file__)
    url = "https://www.romsgames.net/roms/"
    #df = create_console_table(url,path)
    df = pd.read_csv(os.path.join(path, 'provider/tables_romsgames/Console_table.csv'))
    #create_game_table(df.iloc[65:],path)
    util.create_general_table('tables_romsgames')

def random_header():
    '''
    Get a random header for every consult, in this way avoid getting the 
    ip banned
    
    '''

    user_agent_list = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36',
    ]
    user_agent = random.choice(user_agent_list)

    return user_agent  

def create_console_table(url,path):
    '''
    This function is the main part to generate the table of consoles and their url
    in the romsgames site.
    
    path: tha path of the file, is setted in the def romsgames_request()

    url: romsgames url, is setted in the def romsgames_request() 
    

    '''
    headers = {'User-Agent': random_header()}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')

    consoles_pag = str(soup.findAll('ul', class_= 'rg-gamelist rg-consolelist'))

    consoles_table = {
        'console': get_console_name(consoles_pag),
        'link':get_consoles_pages(consoles_pag),
        'site':'https://www.romsgames.net/'
    }

    df = pd.DataFrame(consoles_table)
    df.to_csv(os.path.join(path, 'provider/tables_romsgames/Console_table.csv'),index=False)

    return df

def get_consoles_pages(raw):
    '''
    This function is used to receive the raw text that is generated from 
    The consult on the consoles pages and then, extract the link where there
    is the games links for that consoles page  
    
    '''
    indexes = [m.start() for m in re.finditer('href=', raw)]
    console_link = []
    for index in indexes:
        #temp is used to find the url part
        temp = raw[index+6:index+200].split('"')
        #Itś needed to add that string part because the way it's saved only show
        #the sub part of the domain
        console_link.append('https://www.romsgames.net'+temp[0])
    
    return console_link 

def get_console_name(raw):
    indexes = [m.start() for m in re.finditer('<span>', raw)]
    console_name = []
    for index in indexes:
        temp = raw[index:index+100]
        temp = re.search('<span>(.*)</span>',str(temp)).group(1)
        console_name.append(temp)
    
    return console_name

def create_game_table(df,path):
    for index,row in df.iterrows(): #Here i get the console link
        print(f'colleting game list from {row["console"]} - {index+1} from {len(df)+1}')
        table = get_games_link(row['console'],row['link']) #Call this to itterate to get 
        # in of a console game in ever page, returning that console's games info
        df_temp = pd.DataFrame(table)
        df_temp.to_csv(os.path.join(path, f'provider/tables_romsgames/games_table_{row["console"]}.csv'),index=False)
        print(f'Saved the csv file of {row["console"]}')

def get_games_link(console,console_link):
    '''
    After received a console page link, than iterate in every page
    that have games for a consoles  

    Than create a dictionary that will be used to save the game infos
    in a csv file
    '''
    headers = {'User-Agent': random_header()}
    r = requests.get(console_link,headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    console_games_table = {
        'name':[],
        'console':console,
        'region':[],
        'rating':[],
        'size':[],
        'link':[],
        'site':'https://www.romsgames.net/'
    }
    last_page = get_last_page(soup)
    for pag in range(1,last_page+1):
        print(f'getting pag {pag} of {last_page} - {console}')
        url = console_link + f'?letter=all&page={pag}&sort=popularity'
        temp = consult_console_pag(url) #Get the list of game links in a console page
        game_info = get_game_info(temp)
        console_games_table['name'] = console_games_table['name'] + game_info['name']
        console_games_table['region'] = console_games_table['region'] + game_info['region']
        console_games_table['rating'] = console_games_table['rating'] + game_info['rating']
        console_games_table['size'] = console_games_table['size'] + game_info['size']
        console_games_table['link'] = console_games_table['link'] + game_info['link']
        
    return console_games_table

def get_last_page(soup):
    try: 
        pag_num = str(soup.findAll('ul', class_= 'pagination'))
        temp = re.findall(';page=(.*)&amp;',str(pag_num))
        return int(temp[-1])
    except:
        return 1

def consult_console_pag(url): #Here i get all game link from one page
    headers = {'User-Agent': random_header()}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    raw = str(soup.findAll('ul', class_= 'rg-gamelist'))

    indexes = [m.start() for m in re.finditer('href=', raw)]
    games_link = []
    for index in indexes:
        temp = raw[index+6:index+200].split('"')
        games_link.append('https://www.romsgames.net'+temp[0])

    return games_link

def get_game_info(link_list): #Here, i get all info os games containing in one page\
    table = {
        'name':[],
        'region':[],
        'rating':[],
        'size':[],
        'link':[],
    }
    count = 1
    for link in link_list:
        if (count==1) or (count%6==0):
            print(f'game {count} of {len(link_list)}')
        count+=1
        headers = {'User-Agent': random_header()}
        r = requests.get(link,headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        raw = str(soup.findAll('div', class_= 'rg-gamebox-info'))
        table['name'].append(get_game_name(raw))
        table['region'].append(get_game_region(raw))
        table['rating'].append(get_game_rating(raw))
        table['size'].append(get_game_size(raw))
        table['link'].append(link)

    return table

def get_game_name(raw):
    try:
        temp = re.findall('="name">(.*)</h1>',str(raw))
        return temp[0]
    except:
        return 'none'

def get_game_region(raw):
    try:
        temp = re.findall('alt="(.*)" class',str(raw))
        return temp[0]
    except:
        return 'none'

def get_game_rating(raw):
    try:
        temp_1 = re.findall('rating="(.*)" rati',str(raw))
        temp_2 = re.findall('display">(.*)</span>',str(raw))
        temp = f'{temp_1[0]} ({temp_2[0]} votes)'
        return temp
    except:
        return 'none'

def get_game_size(raw):
    try:
        temp = re.findall('<li>(.*)</li>',str(raw))
        return temp[0]
    except:
        return 'none'






