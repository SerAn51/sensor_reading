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

    try:
        cursor.execute(
            "INSERT INTO sensor_readings (timestamp, humidity, temperature) VALUES (%s, %s, %s)",
            (timestamp, humidity, temperature)
        )
        conn.commit()
        return jsonify({"message": "Dati inseriti con successo"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return 'Server attivo!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
