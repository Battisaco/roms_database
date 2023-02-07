import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os


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
            
            info = get_game_info(link,headers)
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
        df.to_csv(os.path.join(os.path.dirname(__file__), f'provider/tables_romsfun/games_table_{console_name}.csv'),index=False)
        
def create_console_table(console,console_link):
    temp = {'console':console,
            'link':console_link,
            'site':'ROMSFUN.com'}

    df = pd.DataFrame(temp)
    df.to_csv(os.path.join(os.path.dirname(__file__), 'provider/tables_romsfun/Console_table.csv'),index=False)

def console_loop(console_link,headers):
    game_links = []
    for aux_console_link in console_link:
        print(f'Start get game_link for {aux_console_link}')
        game_links.append(get_game_link(aux_console_link,headers))

    create_game_table(game_links,headers)

def get_game_info(game_link,headers):
    #time.sleep(0.5)
    r = requests.get(game_link,headers=headers)    
    soup = BeautifulSoup(r.content, 'html5lib')

    name = get_info_name(soup)
    rate = get_info_rate(soup)
    general = str(soup.find('table', class_= 'table table-borderless table-striped table-sm'))

    console   = get_info_console(general)
    print(name,console)
    publisher = get_info_publisher(general)
    genre     = get_info_genre(general)
    region    = get_info_region(general)
    views     = get_info_views(general)
    downloads = get_info_downloads(general)
    released  = get_info_released(general)

    info_list = [name,rate,console,publisher,
                genre,region,views,downloads,released]

    return info_list

def get_info_console(general_info):
    try:
        index = [m.start() for m in re.finditer('Console', general_info)][0]
        console = (general_info[index:index+150])
        console = re.search('>\n(.*) <',str(console)).group(1)
    except:
        console = 'None'
    return console

def get_info_publisher(general_info):
    try:
        index = [m.start() for m in re.finditer('publisher', general_info)][0]
        publisher = (general_info[index:index+150])
        publisher = str(publisher).split('\n')[1]
    except:
        publisher = 'None'

    return publisher

def get_info_genre(general_info):

    try:
        index = [m.start() for m in re.finditer('genre', general_info)][0]
        genre = (general_info[index:index+150])#.replace("\n", "")
        genre = re.findall('genre=(.*)"',str(genre))
    except:
        genre = 'None'
    return genre

def get_info_region(general_info):
    try:
        index = [m.start() for m in re.finditer('region', general_info)][0]
        region = (general_info[index:index+150])
        region = str(region).split('\n')[1]
    except:
        region = 'None'

    return region

def get_info_views(general_info):
    try:
        index = [m.start() for m in re.finditer('Views', general_info)][0]
        views = (general_info[index:index+150])
        views = re.search('<td>(.*)</td>',str(views)).group(1)
    except:
        views = 'None'
    return views

def get_info_downloads(general_info):
    try:
        index = [m.start() for m in re.finditer('Downloads', general_info)][0]
        downloads = (general_info[index:index+150])
        downloads = re.search('<td>(.*)</td>',str(downloads)).group(1)
    except:
        downloads = 'None'
    return downloads

def get_info_released(general_info):
    try:
        index = [m.start() for m in re.finditer('Released', general_info)][0]
        released = (general_info[index:index+150])
        released = re.search('<td>(.*)</td>',str(released)).group(1)
    except:
        released = 'None'
    return released

def get_info_name(soup):
    try:
        name = soup.select('.text-primary.mb-3')
        name = str(name).split('\n')[1]
    except:
        name = 'None'

    return name

def get_info_rate(soup):
    try:
        rate = soup.select('.ml-2')
        rate = str(rate).split('\n')[1]
    except:
        rate = 'None'
    
    return rate

def romsfun_request():
    url = "https://romsfun.com/roms"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    consoles = get_consoles(url,headers)
    consoles_link = get_consoles_link(url,headers)

    create_console_table(consoles,consoles_link)

    console_loop(consoles_link,headers) 

def create_general_table():
    csv_path = os.path.join(os.path.dirname(__file__), f'provider/tables_romsfun/')
    #get all csv files and ignoring the first (the console table)
    file_list = os.listdir(csv_path)
    df_general = pd.DataFrame()
    #general all files together
    for file in file_list:
        if 'game' in file: 
            temp = pd.read_csv(csv_path + file)
            df_general = pd.concat([df_general,temp], ignore_index=True)
        else:
            pass
    df_general.to_csv(csv_path+'games_table_general.csv',index=False)
