# -*- coding: utf-8 -*-
"""
Muscle Milk

A script to pull a muscle's "code", region, origin, insertion, action, and nerve from http://www.lumen.luc.edu/lumen/meded/grossanatomy/dissector/mml/mmlalpha.htm.

@author: jedraynes
"""

# import packages
import sys
import re
import requests
import pprint
import pandas as pd
from bs4 import BeautifulSoup

# open the html text file of the muscle codes
textfile = open('C:\\Users\\jraynes001\\Documents\\Training\\Python Training\\Personal Projects\\Muscle Milk\\code_html.txt', 'r')

# regex to get alphabetical codes
codes =  re.findall("\=\"(.*.htm)", textfile.read())

# remove the last couple unneeded and add the code not added
codes = codes[:-1]
codes.append("zmn.htm")
print(len(codes))

# bs4
url = 'http://www.lumen.luc.edu/lumen/meded/grossanatomy/dissector/mml/'
muscle_milk = []
count = 0

# for loop to append details to list
for muscle_code in codes:
    html = requests.get(url + muscle_code).text
    soup = BeautifulSoup(html, 'lxml')
    details = []
    try:       
        # muscle code
        details.append(muscle_code[:-4])
        
        # muscle
        muscle = soup.body.b.font.font.font.contents[0]
        details.append(muscle)

        # define the OIAN table range
        rows = soup.find_all('tr')
        
        # origin
        origin = rows[0].td.font.font.contents[0]
        details.append(origin)
        
        # insertion
        insertion = rows[1].td.font.font.contents[0]
        details.append(insertion)
        
        # action
        action = rows[2].td.font.font.contents[0]
        details.append(action)
        
        # nerve
        nerve = rows[3].td.font.font.contents[0]
        details.append(nerve)
        
        # append to main list
        muscle_milk.append(details)
        
        count+=1
        print(str(count) +" " + muscle_code[:-4])
    except:
        # muscle code
        details.append(muscle_code[:-4])        
        
        # muscle
        muscle = soup.body.b.contents[0]
        details.append(muscle)

        # define the OIAN table range
        rows = soup.find_all('tr')
        
        # origin
        origin = rows[0].td.font.font.contents[0]
        details.append(origin)
        
        # insertion
        insertion = rows[1].td.font.font.contents[0]
        details.append(insertion)
        
        # action
        action = rows[2].td.font.font.contents[0]
        details.append(action)
        
        # nerve
        nerve = rows[3].td.font.font.contents[0]
        details.append(nerve)
        
        # append to main list
        muscle_milk.append(details)
        
        count+=1
        print(str(count) +" " + muscle_code[:-4])

# create dataframe
df_details = pd.DataFrame(muscle_milk, columns = ['muscle_code', 'muscle', 'origin', 'insertion', 'action', 'nerve', 'drop'])
df_details.drop(columns = 'drop', inplace = True)

# clean df
for col in df_details.columns:
    # lowercase
    df_details[col] = df_details[col].str.lower()
    # remove line breaks
    df_details[col] = df_details[col].str.replace('\r\n',' ')

# define regions
regions = ['back', 'upper', 'headneck', 'thorax', 'abdomen', 'pelvis', 'lower']

# for loop to create a list of muscle codes and its respective region
region_list = []
for region in regions:
    html = requests.get(url + region + '.htm').text
    soup = BeautifulSoup(html, 'lxml')
    for a in soup.find_all('a', href = True):
        sub_list = []
        region_code = a['href']
        sub_list.append(region_code[:-4])
        region_label = region
        sub_list.append(region_label)
        region_list.append(sub_list)

# create datafram
df_code_by_region = pd.DataFrame(region_list, columns = ['muscle_code', 'region'])

# merge by code
df = pd.merge(df_details, df_code_by_region, on = 'muscle_code', how = 'left')

# inspect for nulls
df.info()
print(df[df['region'].isnull()])

# correct null value
df.loc[df['region'].isnull(), 'region'] = 'headneck'
df.info()

# save df as excel
path = 'C:\\Users\\jraynes001\\Documents\\Training\\Python Training\\Personal Projects\\Muscle Milk\\'
confirm = input('Save the file as .xlsx? y/n: ')
if confirm == 'y':
    df.to_excel(path + 'musclemilk.xlsx', index = False)
    print('Saved!')
else:
    print('Script canceled. Exiting...')
    sys.exit()
