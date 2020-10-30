import os
from flask import Flask
# from scraper import Blacklist
# import scraper
import requests
from bs4 import BeautifulSoup
import pandas as pd

class Blacklist():
    def __init__(self):

        
        self.blacklist = pd.read_json('blacklist.json')
        return

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

        self.blacklist = pd.concat(df)
        self.blacklist['title'] = self.blacklist['title'].str.replace(r'\"', '')
        self.blacklist['title'] = self.blacklist['title'].str.replace(r'\[(\w*\s*\w*)\]', '')
        self.blacklist['blacklist_guide'] = self.blacklist['blacklist_guide'].str.replace(r'(Nos?\.\s)', '')
        
        # Changes the name of the first episode ("Pilot") to its blacklister
        self.blacklist.head(1)['title'] = 'Ranko Zamani'

        self.blacklist.reset_index(drop=True, inplace=True)
        
        # return blacklist

        with open("blacklist.csv", "w") as writer:
            writer.write(self.blacklist.to_csv())
            

    def cut_list(self, episode):
        """
            Cuts the list to remove the user's unseen episodes
        """
        self.blacklist = self.blacklist.loc[0:episode-1]

    def removes_the_conclusions(self):
        """
            Removes all the episodes that are the conclusion of a previous one, thus sharing the same blacklister
        """
        # Slice the conclusions
        conclusions = self.blacklist['title'].str.contains(r'(Conclusion)')

        # Get the list without the sliced conclusions
        self.blacklist = self.blacklist[~conclusions]

    def removes_episodes_without_blacklisters(self):
        """
            Removes all the episodes that dont't have a number in the blacklist
        """
        # Drop all the NaN values
        self.blacklist = self.blacklist.dropna()

    def split_characters(self):

        self.blacklist['blacklist_guide'] = self.blacklist['blacklist_guide'].str.split(pat=r'[/-]')

        new_serie = []

        for row in self.blacklist['blacklist_guide']:
            aux = row
            # print(row)

            if len(row) == 2:
                row = [int(i) for i in row]
                value = [(y - x) for (x, y) in zip(row[:-1], row[1:])]
            
                if value[0] > 1:
                    aux = []
                    cont = value[0]
                    while cont >= 0:
                        aux.append(row[-1] - cont)
                        cont = cont - 1

                        aux = [str(i) for i in aux]
            
            new_serie.append(aux)

            # print(len(new_serie))
            
        self.blacklist['blacklist_guide'] = new_serie

    def order_by_number_in_guide(self):
        self.blacklist = self.blacklist.sort_values(by=['blacklist_guide'])

    def run(self, episode):
        self.cut_list(episode)
        self.removes_the_conclusions()
        self.removes_episodes_without_blacklisters()
        self.split_characters()
        self.order_by_number_in_guide()

        blacklist_json = self.blacklist.to_json(orient='records')
        return blacklist_json


app = Flask(__name__)

@app.route('/<overall_episode>')
def index(overall_episode):
    blacklist = Blacklist()

    # In order to use the Json Formatter Chrome extension
    response = app.response_class(
        response=blacklist.run(int(overall_episode)),
        status=200,
        mimetype='application/json'
    )

    return response
    # return blacklist.run(100)

@app.route('/list')
def blacklist():
    return 'Funcionou!'
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)