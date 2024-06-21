import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_radio_environment_map_from_csv(csv_file):
    # Read data from CSV file
    data = pd.read_excel(csv_file)
    latitudes = data['Latitude'].values
    longitudes = data['Longitude'].values
    signal_strength = data['Amplitude'].values
    # frequencies = data['Frequency'].values

    return latitudes, longitudes, signal_strength

def generate_spectrogram(latitudes, longitudes, signal_strength, target_frequency=470e6):
    # Determine grid resolution
    grid_resolution = 20
    min_lat, max_lat = min(latitudes), max(latitudes)
    min_lon, max_lon = min(longitudes), max(longitudes)
    min_rss, max_rss = min(signal_strength), max(signal_strength)
    lat_grid = np.linspace(min_lat, max_lat, grid_resolution)
    lon_grid = np.linspace(min_lon, max_lon, grid_resolution)

    # Create empty grid for signal strength
    grid = np.zeros((grid_resolution, grid_resolution)) * np.nan

    # Populate grid with signal strengths at nearest grid points
    for lat, lon, strength in zip(latitudes, longitudes, signal_strength):
        lat_index = int((lat - min_lat) / (max_lat - min_lat) * (grid_resolution - 1))
        lon_index = int((lon - min_lon) / (max_lon - min_lon) * (grid_resolution - 1))
        grid[lat_index, lon_index] = strength

    # Plot the spectrogram
    plt.figure(figsize=(20, 10))
    # plt.imshow(grid, extent=( min_lat, max_lat, min_lon, max_lon), cmap='coolwarm', origin='lower', vmin=min_rss, vmax=max_rss)
    plt.imshow(grid, extent=(min_lon, max_lon, min_lat, max_lat), cmap='coolwarm', origin='lower', vmin=min_rss, vmax=max_rss)
    plt.colorbar(label='Signal Strength (dB)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Radio environment map before interpolation for channel 12')
    plt.grid(False)
    plt.show()

# Path to the CSV file containing the data
csv_file = 'Channel 12_F1.xlsx'

# Read radio environment map data from CSV
latitudes, longitudes, signal_strength = read_radio_environment_map_from_csv(csv_file)

# Generate and display spectrogram for the target frequency (470MHz)
generate_spectrogram(latitudes, longitudes, signal_strength, target_frequency=470e6)
