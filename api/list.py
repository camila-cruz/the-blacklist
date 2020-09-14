from flask import Flask
import scraper

app = Flask(__name__)

@app.route('/')
def index():
    return scraper.run(100)

@app.route('/list')
def blacklist():
    return 'Funcionou!'
    
if __name__ == '__main__':
    app.run(debug=True)
