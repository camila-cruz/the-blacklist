from flask import Flask
from flask_cors import CORS
# from scraper import Blacklist
import scraper

app = Flask(__name__)
CORS(app)

@app.route('/<overall_episode>')
def index(overall_episode):
    blacklist = scraper.Blacklist()

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
    
if __name__ == '__main__':
    app.run(debug=True)
