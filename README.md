# Progetto di Scraping Auto

Questo progetto esegue lo scraping delle offerte di auto dal sito Finrent e le espone tramite un'API Flask.

## Installazione

Per eseguire questo progetto, è consigliabile utilizzare un ambiente virtuale Python.

1.  **Clona il repository**
    ```
    git clone https://github.com/Signoregregio/scraping_finrent.git
    ```

2.  **Crea e attiva un ambiente virtuale**
    ```
    # Su Windows
    python -m venv venv
    .\venv\Scripts\Activate.ps1

    # Su macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Installa le dipendenze**
    Questo comando installerà tutte le librerie necessarie dal file `requirements.txt`.
    ```
    pip install -r requirements.txt
    ```

## Generare dipendenze

### 1. Backup del file attuale
cp requirements.txt requirements_backup.txt

### 2. Installa e usa pipreqs
pip install pipreqs
pipreqs . --force

### 3. Controlla il risultato
cat requirements.txt

### 4. Testa che funzioni tutto
pip install -r requirements.txt


## Esecuzione

Per avviare il server Flask, esegui:
```
python app.py
```
L'API sarà disponibile all'indirizzo `http://127.0.0.1:5000/data`.
```
Lancio comando: 

L'applicativo è disponibile all'indirizzo http://127.0.0.1:5000/
***
