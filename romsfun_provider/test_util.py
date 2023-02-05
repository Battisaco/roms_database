import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time

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




