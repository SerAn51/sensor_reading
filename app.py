from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

# Connessione al database Railway
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    port=os.getenv('DB_PORT')
)
cursor = conn.cursor()

@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    timestamp = data.get('timestamp')

    # Se non c'è timestamp dal client, usa quello del server (non dovrebbe succedere mai)
    if not timestamp:
        timestamp = datetime.utcnow().isoformat()
    else:
        # Verifica se il timestamp è un intero (Unix timestamp)
        try:
            # Se è una stringa, prova a convertirla in intero
            if isinstance(timestamp, str):
                timestamp = int(timestamp)
            
            # Se è un timestamp Unix (numero di secondi), convertilo in formato ISO 8601
            if isinstance(timestamp, int) or isinstance(timestamp, float):
                timestamp = datetime.utcfromtimestamp(timestamp).isoformat()
        except (ValueError, TypeError):
            return jsonify({"error": "Timestamp non valido"}), 400

    try:
        cursor.execute(
            "INSERT INTO sensor_readings (time, humidity, temperature) VALUES (%s, %s, %s)",
            (timestamp, humidity, temperature)
        )
        conn.commit()
        return jsonify({"message": "Dati inseriti con successo"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    # DEBUG - verifica che i dati arrivino
    #html = f"""
    #    <h1>Dati ricevuti</h1>
    #    <p><strong>Temperatura:</strong> {temperature}°C</p>
    #    <p><strong>Umidità:</strong> {humidity}%</p>
    #    <p><strong>Timestamp:</strong> {timestamp}</p>
    #"""
    #return html

@app.route('/')
def home():
    return 'Server attivo!'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
