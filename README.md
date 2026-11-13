# Weather Data Analysis Using Python

A complete Python project for analyzing historical weather data.  
This project fetches real weather data, performs statistical analysis, and generates visualizations.

## Features

- Fetches historical weather data using the free **Open-Meteo API** (no API key required)
- Analyzes temperature trends, humidity, precipitation, and wind speed
- Generates summary statistics
- Creates visualizations (temperature trends, rainfall distribution, etc.)
- Saves cleaned data and analysis results

## Project Structure

```
weather-data-analysis-using-python/
├── README.md
├── requirements.txt
├── weather_analysis.py          # Main analysis script
├── data/                        # Folder for downloaded/processed data
└── outputs/                     # Folder for plots and result files
```

## Requirements

- Python 3.8+
- Libraries listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Chimcdonald/weather-data-analysis-using-python.git
cd weather-data-analysis-using-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

```bash
python weather_analysis.py
```

The script will:
1. Download historical weather data for a selected city (default: Delhi)
2. Perform analysis
3. Print summary statistics in the terminal
4. Save plots and CSV files in the `outputs/` folder

## Sample Output (Summary Statistics)

```
=== Weather Data Analysis Summary ===
Location: Delhi, India
Period: Last 365 days

Temperature (°C):
  Average: 26.4
  Maximum: 42.1
  Minimum: 7.8

Precipitation (mm):
  Total rainfall: 842.3
  Rainy days: 87

Humidity (%):
  Average: 58.2
```

## Customization

You can change the city by modifying the latitude, longitude, and city name in `weather_analysis.py`.

## Libraries Used

- `pandas` – Data manipulation
- `matplotlib` & `seaborn` – Visualization
- `requests` – API calls
- `numpy` – Numerical operations

---

**Created for educational purposes**  
Feel free to fork, modify, and use this project.
