import logging
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
db_path = 'example.db'

# Configure logging
logging.basicConfig(filename='backend.log', level=logging.INFO)

def initialize_database():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS example_table
                     (id INTEGER PRIMARY KEY, name TEXT)''')
        conn.commit()
    except sqlite3.Error as e:
        app.logger.error(f"Error initializing database: {e}")
    finally:
        conn.close()

@app.route('/store_data', methods=['POST'])
def store_data():
    data = request.json
    if 'name' not in data:
        app.logger.error('Name field is required')
        return jsonify({'error': 'Name field is required'}), 400

    name = data['name']
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO example_table (name) VALUES (?)", (name,))
            conn.commit()
        app.logger.info('Data stored successfully')
        return jsonify({'message': 'Data stored successfully'}), 200
    except sqlite3.Error as e:
        app.logger.error(f"Error storing data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_data')
def get_data():
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM example_table")
            data = c.fetchall()
        app.logger.info('Data retrieved successfully')
        return jsonify({'data': data}), 200
    except sqlite3.Error as e:
        app.logger.error(f"Error retrieving data: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=5001)


