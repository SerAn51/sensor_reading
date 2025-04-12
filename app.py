from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Connessione al database Railway
conn = psycopg2.connect(
    host="centerbeam.proxy.rlwy.net",
    database="railway",
    user="railway",
    password="1r3ad48055h0p9mpg51aw4r6dv3cqm8m",
    port=28234
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
