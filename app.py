from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

# load .env file
load_dotenv()

# initeialize Flask app
app = Flask(__name__)

# get webhook URL from environment variable
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

# what is the meaning of route '/'
# this is the main page of the app
@app.route('/')
def index():
    return render_template('index.html')

# what is the meaning of route '/flask-chat'
# this is the route that will handle the chat messages
@app.route('/flask-chat', methods=['POST'])
def flask_chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid input'}), 400

        # Route the message to n8n webhook
        response = requests.post(N8N_WEBHOOK_URL, json={'message': data['message']})

        # Return the 'output' key from n8n response
        if response.ok:
            n8n_response = response.json()
            return jsonify({'response': n8n_response.get('output', 'No output found')}), 200
        else:
            return jsonify({'error': 'Failed to get response from n8n', 'details': response.text}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    # localhost for development, deployment change host='0.0.0.0'
    app.run(debug=True)