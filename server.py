from flask import Flask, request, jsonify  # Importa Flask e le funzioni necessarie per gestire le richieste e rispondere con JSON
import re

app = Flask(__name__)  # Crea un'istanza dell'app Flask

data = {                # Un dizionario che fungerà da database in memoria per memorizzare i dati
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3'
}  

@app.route('/')  # Definisce una route di test per la root dell'applicazione
def home():
    return "Server is running!"  # Restituisce un semplice messaggio per confermare che il server è in esecuzione

@app.route('/item/<key>', methods=['GET'])  # Definisce una route per gestire le richieste GET per un item specifico
def get_item(key):
    if key in data:  # Controlla se la chiave esiste nel dizionario
        return jsonify({key: data[key]})  # Restituisce il valore associato alla chiave in formato JSON
    else:
        return "Item not found", 404  # Restituisce un errore 404 se la chiave non esiste

@app.route('/item', methods=['POST'])  # Definisce una route per gestire le richieste POST per creare un nuovo item
def post_item():
    item = request.json  # Ottiene i dati JSON dalla richiesta
    key = item.get('key')  # Estrae la chiave dall'oggetto JSON
    value = item.get('value')  # Estrae il valore dall'oggetto JSON
    x = re.search("key[1-5]", key) #la mia regex
    if key in data:  # Controlla se la chiave esiste già nel dizionario
        return "Item already exists", 400  # Restituisce un errore 400 se la chiave esiste già
    elif x: # se la regex matcha un valore allora esegue sotto
        data[key] = value  # Aggiunge il nuovo item al dizionario
        return jsonify({key: value}), 201  # Restituisce il nuovo item creato in formato JSON con un codice di stato 201
    else: # se la regex non matcha allora restituisci sotto
        return "There can be maximum 5 keys, try again :(", 406 # messaggio per informare l'utente e codice di uscita

@app.route('/item/<key>', methods=['PUT'])  # Definisce una route per gestire le richieste PUT per creare o aggiornare un item specifico
def put_item(key):
    value = request.json.get('value')  # Ottiene il valore dalla richiesta JSON
    data[key] = value  # Aggiorna o crea una nuova voce nel dizionario con la chiave specificata
    return jsonify({key: value}), 201  # Restituisce l'item creato o aggiornato in formato JSON con un codice di stato 201

@app.route('/item/<key>', methods=['PATCH'])  # Definisce una route per gestire le richieste PATCH per aggiornare parzialmente un item specifico
def patch_item(key):
    if key in data:  # Controlla se la chiave esiste nel dizionario
        value = request.json.get('value')  # Ottiene il valore dalla richiesta JSON
        data[key] = value  # Aggiorna il valore della chiave esistente nel dizionario
        return jsonify({key: value})  # Restituisce l'item aggiornato in formato JSON
    else:
        return "Item not found", 404  # Restituisce un errore 404 se la chiave non esiste

@app.route('/item/<key>', methods=['DELETE'])  # Definisce una route per gestire le richieste DELETE per eliminare un item specifico
def delete_item(key):
    if key in data:  # Controlla se la chiave esiste nel dizionario
        del data[key]  # Elimina la voce associata alla chiave dal dizionario
        return '', 204  # Restituisce un codice di stato 204 senza contenuto
    else:
        return "Item not found", 404  # Restituisce un errore 404 se la chiave non esiste

if __name__ == '__main__':  # Verifica se il file viene eseguito direttamente e non importato come modulo
    app.run(debug=True)  # Avvia il server in modalità debug
