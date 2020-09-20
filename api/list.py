from flask import Flask
# from scraper import Blacklist
import scraper

app = Flask(__name__)

@app.route('/')
def index():
    blacklist = scraper.Blacklist()

    # In order to use the Json Formatter Chrome extension
    response = app.response_class(
        response=blacklist.run(152),
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
