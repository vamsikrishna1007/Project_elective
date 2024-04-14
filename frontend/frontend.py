import logging
from flask import Flask, jsonify, request, render_template
from flask import redirect, url_for
import requests

app = Flask(__name__)
backend_url = "http://127.0.0.1:5001"

# Configure logging
logging.basicConfig(filename='frontend.log', level=logging.INFO)

@app.route('/')
def index():
    app.logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/store_data', methods=['POST'])
def store_data():
    name = request.form.get('name')
    if not name:
        app.logger.error('Name is required')
        return jsonify({'error': 'Name is required'}), 400

    data = {'name': name}
    try:
        response = requests.post(f"{backend_url}/store_data", json=data)
        response.raise_for_status()
        app.logger.info('Data stored successfully')
        return redirect(url_for('index'))  # Redirect to the index page
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error storing data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_data')
def get_data():
    try:
        response = requests.get(f"{backend_url}/get_data")
        response.raise_for_status()
        app.logger.info('Data retrieved successfully')
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error retrieving data: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



