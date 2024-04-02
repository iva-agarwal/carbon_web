# app.py

from flask import Flask, request, jsonify
from sample import calculate_footprint  # Importing calculatecarbon function from sample module
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculatecarbon', methods=['POST'])
def calculate_carbon():
    data = request.json
    web_url = data.get('url')
    result = calculate_footprint(web_url)  # Using calculatecarbon function
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
