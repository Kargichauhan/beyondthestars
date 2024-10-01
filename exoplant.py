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

def get_exoplanet_data():
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    params = {
        "query": "SELECT pl_name FROM ps ORDER BY pl_name",
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

def main():
    exoplanets = get_exoplanet_data()
    
    if not exoplanets:
        print("No exoplanet data available. Exiting.")
        return

    total_planets = len(exoplanets)
    print(f"Total exoplanets: {total_planets}")
    
    print("\nList of all exoplanets:")
    for i, planet in enumerate(exoplanets, 1):
        print(f"{i}. {planet['pl_name']}")

    while True:
        try:
            choice = int(input("\nSelect an exoplanet (enter the number): "))
            selected = exoplanets[choice - 1]['pl_name']
            print(f"\nSelected exoplanet: {selected}")
            break
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number from the list.")

if __name__ == "__main__":
    main()