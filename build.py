import os
from flask import Flask, request, jsonify, render_template
import openai
import requests

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = os.getenv('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')

# Set your Google Custom Search API key and Search Engine ID here
google_api_key = os.getenv('AIzaSyBCGoHE6yKmZuOW_-L-xL_cproLsP9eSzE')
search_engine_id = os.getenv('46eee31b26f0045b2')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({'response': response.choices[0].message['content'].strip()})
    except Exception as e:
        return jsonify({'response': 'Sorry, something went wrong.'}), 500

@app.route('/websearch', methods=['POST'])
def websearch():
    query = request.json.get('query')
    params = {
        'key': google_api_key,
        'cx': search_engine_id,
        'q': query,
    }
    try:
        response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
        response.raise_for_status()
        search_results = response.json()
        top_result = search_results['items'][0]['snippet']
        return jsonify({'results': top_result})
    except Exception as e:
        return jsonify({'results': 'Sorry, something went wrong with the web search.'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))