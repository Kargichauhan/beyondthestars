from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "id": 1,
        "name": "Sample Item"
    }
    return jsonify(data)

@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.json
    return jsonify({"message": f"Received: {data['name']}"})

if __name__ == '__main__':
    app.run(debug=True)
