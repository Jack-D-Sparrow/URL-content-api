from flask import Flask, request, jsonify
from readability import Document
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/extract', methods=['GET'])
def extract_content():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        doc = Document(response.text)
        soup = BeautifulSoup(doc.summary(), 'html.parser')
        text = soup.get_text(separator='\n').strip()
        return jsonify({
            'title': doc.short_title(),
            'content': text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
