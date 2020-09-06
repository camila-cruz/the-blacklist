import requests
from bs4 import BeautifulSoup
import pandas as pd

# Wikipedia's list of episodes
URL = 'https://en.wikipedia.org/wiki/List_of_The_Blacklist_episodes'

# Wikipedia's page - to see its content, use print(page.content)
page = requests.get(URL)

# BeautifulSoup object that will be used to find stuff in the content
soup = BeautifulSoup(page.content, 'html.parser')

# List with all episode tables
tables = soup.find_all('table', class_='wikiepisodetable')

# parses the BeautifulSoup object into a string, so read_html can be used
tables_str = str(tables)

# list of tables, each table must be accessed by its index
df = pd.read_html(tables_str)

for index, season in enumerate(df):
    season.columns = ['no._overall', 'no_in_season', 'title', 'blacklist_guide', 'directed', 'written', 'air_date', 'viewers']
    season.insert(0, 'season_no', index+1)
    season.drop(columns=['no._overall', 'directed', 'written', 'air_date', 'viewers'], inplace=True)

blacklist = pd.concat(df)
blacklist['title'] = blacklist['title'].str.replace(r'\"', '')
blacklist['title'] = blacklist['title'].str.replace(r'\[(\w*\s*\w*)\]', '')
blacklist['blacklist_guide'] = blacklist['blacklist_guide'].str.replace(r'(Nos?\.\s)', '')

blacklist.reset_index(drop=True, inplace=True)
blacklist_json = blacklist.to_json(orient='split')

with open("blacklist.json", "w") as writer:
    writer.write(blacklist_json)