from flask import Flask, jsonify, request, render_template
from exoplant import get_exoplanet_data, demonstrate_3d_positioning_for_exoplanet  # Import the function

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

@app.route('/api/exoplanet', methods=['GET'])
def exoplanet():
    data = get_exoplanet_data()  # Call the function
    print("\n3D Positioning Demonstration for an Exoplanet:")
    print(demonstrate_3d_positioning_for_exoplanet())
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
