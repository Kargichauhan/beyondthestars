"""
Exoplanet Selection Console App

This script generates a simple console application that allows users to select an exoplanet from a list.
It fetches all exoplanet names from the NASA Exoplanet Archive, displays the complete list to the user,
and allows them to choose one exoplanet to view.

The app demonstrates basic API interaction, data parsing, and user input handling in a console environment.
"""
# python3 -m venv exosky_env
# source exosky_env/bin/activate
# pip3 install requests
import requests
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord, Distance
import astropy.units as u

def get_exoplanet_data():
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    params = {
        "query": "SELECT pl_name, ra, dec FROM ps ORDER BY pl_name",
        "format": "json"
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        print("Response content:")
        print(response.text)
        return []

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Unable to parse JSON response")
        print("Response content:")
        print(response.text)
        return []

def convert_coordinates(ra, dec, parallax):
    distance = Distance(parallax=parallax * u.mas).pc
    coord = SkyCoord(ra, dec, distance=distance, unit=('deg', 'deg', 'pc'), frame='icrs')
    return coord.cartesian.x.value, coord.cartesian.y.value, coord.cartesian.z.value

def get_stars_near_exoplanet(exoplanet_ra, exoplanet_dec, max_stars=10, radius_deg=0.1):
    query = f"""SELECT TOP {max_stars} source_id, ra, dec, parallax
                FROM gaiadr3.gaia_source
                WHERE 1=CONTAINS(POINT('ICRS', ra, dec),
                    CIRCLE('ICRS', {exoplanet_ra}, {exoplanet_dec}, {radius_deg}))
                AND parallax > 0
                """

    job = Gaia.launch_job_async(query)
    return job.get_results()

def demonstrate_3d_positioning_for_exoplanet():
    exoplanet_name = "Example Exoplanet"
    exoplanet_ra = 266.41683
    exoplanet_dec = -29.00781

    print(f"Demonstrating 3D positioning for stars near {exoplanet_name}")
    print(f"Exoplanet coordinates: RA = {exoplanet_ra}, Dec = {exoplanet_dec}")

    nearby_stars = get_stars_near_exoplanet(exoplanet_ra, exoplanet_dec, max_stars=10, radius_deg=0.5)
    print(f"Number of stars found near {exoplanet_name}: {len(nearby_stars)}")

    if len(nearby_stars) > 0:
        print(f"Nearby stars (up to {len(nearby_stars)}):")
        for i, star in enumerate(nearby_stars):
            x, y, z = convert_coordinates(star['ra'], star['dec'], star['parallax'])
            print(f"Star {i+1}: x={x:.2f}, y={y:.2f}, z={z:.2f} parsecs")
    else:
        print("No stars found with reliable parallax data near this exoplanet.")