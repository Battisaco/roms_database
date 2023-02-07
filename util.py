import pandas as pd
import os

def to_txt(text):
    file = open("html_analysis.txt", "w")
    a = file.write(str(text))
    file.close()

def create_general_table(site):
    csv_path = os.path.join(os.path.dirname(__file__), f'provider/{site}/')
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
