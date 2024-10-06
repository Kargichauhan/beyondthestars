from flask import Flask, jsonify, redirect, request, render_template, url_for
from exoplant import get_exoplanet_data, demonstrate_3d_positioning_for_exoplanet, showStars  # Import the function
from flask import send_file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/earth')
def earth():
    return send_file('./earth.jpg', mimetype='image/jpg')

@app.route('/venus')
def venus():
    return send_file('./venus.jpg', mimetype='image/jpg')

@app.route('/mercury')
def mercury():
    return send_file('./mercury.jpg', mimetype='image/jpg')

@app.route('/makemake')
def makemake():
    return send_file('./makemake.jpg', mimetype='image/jpg')

@app.route('/haumea')
def haumea():
    return send_file('./haumea.jpg', mimetype='image/jpg')

@app.route('/uranus')
def uranus():
    return send_file('./uranus.jpg', mimetype='image/jpg')

@app.route('/ceres')
def ceres():
    return send_file('./ceres.jpg', mimetype='image/jpg')

@app.route('/mars')
def mars():
    return send_file('./mars.jpg', mimetype='image/jpg')


@app.route('/threed')
def threed():
    return render_template('threedplanet.html')

@app.route('/exosky')
def exosky():
    return render_template('exosky.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/team')
def team():
    return render_template('team.html')

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


# Route to render the Star Chart page
@app.route('/starchart')
def star_chart():
    # Get RA and Dec from query parameters (or provide default for demo)
    ra = float(request.args.get('ra', 266.41683))
    dec = float(request.args.get('dec', -29.00781))

    # Get star data (you could also pass data here directly)
    star_data = showStars(ra, dec)
    print(star_data)

    # Pass the star data to the template where you can render the star chart
    return render_template('starchart.html', star_data=star_data)


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
