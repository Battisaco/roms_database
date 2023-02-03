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

    r = requests.get(console_link,headers=headers)
    
    soup = BeautifulSoup(r.content, 'html5lib')
    raw = str(soup.find_all('a', class_="text-center bg-white border rounded shadow-sm d-flex flex-column h-100 p-3")) 

    indexes = [m.start() for m in re.finditer('href=', raw)]
    game_link = []
    
    for index in indexes:
        temp = raw[index+6:index+200].split('"')
        game_link.append(temp[0])

    return game_link

def create_console_table(console,console_link):
    temp = {'Console':console,
            'Link':console_link}

    df = pd.DataFrame(temp)
    df.to_csv(os.path.join(os.path.dirname(__file__), 'Console_table.csv'),index=False)
    