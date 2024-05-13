from flask import Flask, request, jsonify
from PyComponent import analyze_python_code

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if 'code' not in data:
        return jsonify({'error': 'Please provide code to analyze'}), 400
    
    code = data['code']
    result = analyze_python_code(code)
    
    return result, 200

if __name__ == '__main__':
    app.run(debug=True)
