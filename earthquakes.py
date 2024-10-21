from datetime import date
import matplotlib.pyplot as plt
import requests

def get_data():
    """Retrieve the earthquake data from USGS."""
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'
    response = requests.get(url)
    data = response.json()
    return data

def get_year(earthquake):
    """Extract the year from the earthquake timestamp."""
    timestamp = earthquake['properties']['time']
    year = date.fromtimestamp(timestamp / 1000).year
    return year

def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake."""
    return earthquake['properties']['mag']

def get_magnitudes_per_year(earthquakes):
    """Retrieve earthquake magnitudes grouped by year."""
    magnitudes_per_year = {}
    for quake in earthquakes:
        year = get_year(quake)
        magnitude = get_magnitude(quake)

        if magnitude is not None:
            if year in magnitudes_per_year:
                magnitudes_per_year[year].append(magnitude)
            else:
                magnitudes_per_year[year] = [magnitude]
    return magnitudes_per_year

def plot_average_magnitude_per_year(earthquakes):
    """Plot the average magnitude of earthquakes per year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())
    average_magnitudes = [sum(magnitudes_per_year[year]) / len(magnitudes_per_year[year]) for year in years]

    plt.figure(figsize=(10, 6))
    plt.plot(years, average_magnitudes, marker='o', linestyle='-', color='red')
    plt.title('Average Magnitude of Earthquakes Per Year')
    plt.xlabel('Year')
    plt.ylabel('Average Magnitude')
    plt.grid(True)
    plt.show()

def plot_number_per_year(earthquakes):
    """Plot the number of earthquakes per year."""
    quakes_per_year = {}
    for quake in earthquakes:
        year = get_year(quake)
        if year in quakes_per_year:
            quakes_per_year[year] += 1
        else:
            quakes_per_year[year] = 1

    years = sorted(quakes_per_year.keys())
    numbers = [quakes_per_year[year] for year in years]

    plt.figure(figsize=(10, 6))
    plt.bar(years, numbers, color='blue')
    plt.title('Number of Earthquakes Per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.grid(True)
    plt.show()

# Retrieve and process earthquake data
quakes = get_data()['features']

# Debugging step: Check if data is loaded correctly
print(f"Number of earthquakes: {len(quakes)}")

# Generate and show plots
plot_number_per_year(quakes)
plt.clf()  # Clear the figure for the next plot
plot_average_magnitude_per_year(quakes)
