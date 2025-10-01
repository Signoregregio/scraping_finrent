from flask import Flask, jsonify
from flask_cors import CORS
import json
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse, quote
from scraper import esegui_scraping


app = Flask(
    __name__,
    static_folder='static',  # Cartella con HTML, JS, CSS
    static_url_path=''       # Svuota il prefisso URL, così funziona tutto su root
)

@app.route('/data')
def data():
    result = esegui_scraping()
    return jsonify(result)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)

