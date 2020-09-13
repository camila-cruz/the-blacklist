import requests
from bs4 import BeautifulSoup
import pandas as pd

def scraper():
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
        season.columns = ['no_overall', 'no_in_season', 'title', 'blacklist_guide', 'directed', 'written', 'air_date', 'viewers']
        season.insert(0, 'season_no', index+1)
        season.drop(columns=['no_overall', 'directed', 'written', 'air_date', 'viewers'], inplace=True)

    blacklist = pd.concat(df)
    blacklist['title'] = blacklist['title'].str.replace(r'\"', '')
    blacklist['title'] = blacklist['title'].str.replace(r'\[(\w*\s*\w*)\]', '')
    blacklist['blacklist_guide'] = blacklist['blacklist_guide'].str.replace(r'(Nos?\.\s)', '')
    
    # Changes the name of the first episode ("Pilot") to its blacklister
    blacklist.head(1)['title'] = 'Ranko Zamani'

    blacklist.reset_index(drop=True, inplace=True)
    
    return blacklist

    # with open("blacklist.json", "w") as writer:
    #     writer.write(blacklist_json)

def cut_list(episode, blacklist):
    """
        Cuts the list to remove the user's unseen episodes
    """
    return blacklist.loc[0:episode-1]

def removes_the_conclusions(blacklist):
    """
        Removes all the episodes that are the conclusion of a previous one, thus sharing the same blacklister
    """
    # Slice the conclusions
    conclusions = blacklist['title'].str.contains(r'(Conclusion)')

    # Get the list without the sliced conclusions
    blacklist = blacklist[~conclusions]

    return blacklist

def removes_episodes_without_blacklisters(blacklist):
    """
        Removes all the episodes that dont't have a number in the blacklist
    """
    # Drop all the NaN values
    return blacklist.dropna()

def split_characters(blacklist):
    pass

def run(episode):
    blacklist = scraper()
    blacklist = cut_list(episode, blacklist)
    blacklist = removes_the_conclusions(blacklist)
    blacklist = removes_episodes_without_blacklisters(blacklist)

    blacklist_json = blacklist.to_json(orient='records')
    return blacklist_json