from flask import Flask, jsonify
from flask_cors import CORS

# 1. Importa la funzione dal tuo file scraping.py
from scraper import esegui_scraping

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le route e tutti i domini

@app.route('/data')
def data():
    # 2. Chiama la funzione di scraping per ottenere i dati
    result = esegui_scraping()
    
    # 3. Restituisci i dati come JSON
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
