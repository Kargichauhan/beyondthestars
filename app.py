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
    return jsonify(data)

@app.route('/api/position', methods=['POST'])
def position():
    data = request.get_json()
    ra = data.get('ra')  # Right Ascension in degrees
    dec = data.get('dec')  # Declination in degrees

    return jsonify(demonstrate_3d_positioning_for_exoplanet(ra, dec))

@app.route('/api/cartesian', methods=['POST'])
def calculate_cartesian():
    data = request.get_json()
    distance = data.get('distance')  # In parsecs or a unit of your choice
    ra = data.get('ra')  # Right Ascension in degrees
    dec = data.get('dec')  # Declination in degrees

    # Convert degrees to radians
    import math
    ra_rad = math.radians(ra)
    dec_rad = math.radians(dec)

    # Calculate Cartesian coordinates
    x = distance * math.cos(dec_rad) * math.cos(ra_rad)
    y = distance * math.cos(dec_rad) * math.sin(ra_rad)
    z = distance * math.sin(dec_rad)

    return jsonify({'x': x, 'y': y, 'z': z})

if __name__ == '__main__':
    app.run(debug=True)
