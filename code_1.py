import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt

def load_exoplanet_data():
    # Replace with the actual path to your CSV file
    exoplanets = pd.read_csv('exoplanet.csv')
    return exoplanets

def load_star_catalog():
    # Replace with the actual path to your CSV file
    stars = pd.read_csv('resultstars.csv')
    return stars

def calculate_star_positions(exoplanet, star_catalog):
    exoplanet_coords = SkyCoord(ra=exoplanet['ra']*u.deg, dec=exoplanet['dec']*u.deg, distance=exoplanet['sy_dist']*u.pc)
    star_coords = SkyCoord(ra=star_catalog['ra']*u.deg, dec=star_catalog['dec']*u.deg, distance=star_catalog['distance']*u.pc)

    new_coords = star_coords.transform_to(exoplanet_coords.skyoffset_frame())

    star_catalog['new_ra'] = new_coords.lon.deg
    star_catalog['new_dec'] = new_coords.lat.deg

    return star_catalog

def create_sky_chart(star_positions, exoplanet_name):
    plt.figure(figsize=(10, 10))
    plt.scatter(star_positions['new_ra'], star_positions['new_dec'],
                s=1/star_positions['absmag'], alpha=0.5)
    plt.xlim(180, -180)
    plt.ylim(-90, 90)
    plt.title(f"Sky Chart from {exoplanet_name}")
    plt.xlabel("Right Ascension")
    plt.ylabel("Declination")
    plt.show()

def create_combined_chart(exoplanets, star_positions):
    plt.figure(figsize=(15, 10))

    plt.scatter(star_positions['ra'], star_positions['dec'],
                s=1/star_positions['absmag'], alpha=0.5, color='lightblue', label='Stars')

    plt.scatter(exoplanets['ra'], exoplanets['dec'],
                s=50, alpha=1, color='red', label='Exoplanets')

    plt.xlim(max(exoplanets['ra']) + 10, min(exoplanets['ra']) - 10)
    plt.ylim(min(exoplanets['dec']) - 10, max(exoplanets['dec']) + 10)
    plt.title("Combined Sky Chart: Exoplanets and Stars")
    plt.xlabel("Right Ascension (degrees)")
    plt.ylabel("Declination (degrees)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def main():
    print("Loading data...")
    exoplanets = load_exoplanet_data()
    stars = load_star_catalog()

    while True:
        print("\nAvailable exoplanets:")
        for i, planet in enumerate(exoplanets['source_id'][:10]):
            print(f"{i+1}. {planet}")

        choice = input("\nEnter the number of the exoplanet you want to view (1-10), or 'q' to quit: ")
        
        if choice.lower() == 'q':
            print("Exiting program.")
            break

        try:
            choice = int(choice) - 1
            if choice < 0 or choice >= 10:
                raise ValueError

            selected_exoplanet = exoplanets.iloc[choice]

            print(f"\nGenerating sky chart for {selected_exoplanet['pl_name']}...")
            star_positions = calculate_star_positions(selected_exoplanet, stars)

            create_sky_chart(star_positions, selected_exoplanet['pl_name'])
            print(f"\nSky chart for {selected_exoplanet['pl_name']} has been displayed.")

            show_combined = input("Would you like to see the combined chart? (y/n): ")
            if show_combined.lower() == 'y':
                create_combined_chart(exoplanets, stars)
                print("Combined chart has been displayed.")

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()