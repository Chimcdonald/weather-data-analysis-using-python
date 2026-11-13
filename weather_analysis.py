"""
Weather Data Analysis Using Python
----------------------------------
This script fetches historical weather data from the free Open-Meteo API,
performs statistical analysis, and generates visualizations.

No API key is required.
"""

import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# ====================== CONFIGURATION ======================
CITY_NAME = "Delhi"
LATITUDE = 28.6139
LONGITUDE = 77.2090
DAYS = 365  # Analyze last 1 year of data

# Create folders if they don't exist
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# ====================== FETCH DATA ==========================
def fetch_weather_data(lat, lon, days=365):
    """Fetch daily historical weather data from Open-Meteo."""
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,"
        f"precipitation_sum,relative_humidity_2m_mean,windspeed_10m_max"
        f"&timezone=auto"
    )

    print(f"Fetching weather data for {CITY_NAME}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    daily = data["daily"]
    df = pd.DataFrame({
        "date": pd.to_datetime(daily["time"]),
        "temp_max": daily["temperature_2m_max"],
        "temp_min": daily["temperature_2m_min"],
        "temp_mean": daily["temperature_2m_mean"],
        "precipitation": daily["precipitation_sum"],
        "humidity": daily["relative_humidity_2m_mean"],
        "wind_max": daily["windspeed_10m_max"]
    })

    return df

# ====================== ANALYSIS ============================
def analyze_data(df):
    """Print and return summary statistics."""
    print("\n" + "=" * 50)
    print("=== Weather Data Analysis Summary ===")
    print("=" * 50)
    print(f"Location      : {CITY_NAME}")
    print(f"Period        : {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Total days    : {len(df)}")
    print()

    print("Temperature (°C):")
    print(f"  Average     : {df['temp_mean'].mean():.1f}")
    print(f"  Maximum     : {df['temp_max'].max():.1f}")
    print(f"  Minimum     : {df['temp_min'].min():.1f}")
    print()

    print("Precipitation (mm):")
    print(f"  Total       : {df['precipitation'].sum():.1f}")
    print(f"  Rainy days  : {(df['precipitation'] > 0).sum()}")
    print(f"  Max in a day: {df['precipitation'].max():.1f}")
    print()

    print("Humidity (%):")
    print(f"  Average     : {df['humidity'].mean():.1f}")
    print()

    print("Wind Speed (km/h):")
    print(f"  Max recorded: {df['wind_max'].max():.1f}")
    print("=" * 50)

    return {
        "avg_temp": round(df['temp_mean'].mean(), 1),
        "max_temp": round(df['temp_max'].max(), 1),
        "min_temp": round(df['temp_min'].min(), 1),
        "total_rain": round(df['precipitation'].sum(), 1),
        "rainy_days": int((df['precipitation'] > 0).sum()),
        "avg_humidity": round(df['humidity'].mean(), 1)
    }

# ====================== VISUALIZATIONS ======================
def create_visualizations(df):
    """Generate and save analysis plots."""
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = (12, 6)

    # 1. Temperature Trend
    plt.figure()
    plt.plot(df["date"], df["temp_max"], label="Max Temp", color="#e74c3c", alpha=0.8)
    plt.plot(df["date"], df["temp_min"], label="Min Temp", color="#3498db", alpha=0.8)
    plt.fill_between(df["date"], df["temp_min"], df["temp_max"], color="#95a5a6", alpha=0.2)
    plt.title(f"Daily Temperature Trend - {CITY_NAME}", fontsize=14, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/temperature_trend.png", dpi=150)
    plt.close()
    print("Saved: outputs/temperature_trend.png")

    # 2. Monthly Average Temperature
    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("month")[["temp_mean", "precipitation"]].mean().reset_index()
    monthly["month"] = monthly["month"].astype(str)

    plt.figure()
    sns.barplot(data=monthly, x="month", y="temp_mean", color="#e67e22")
    plt.title(f"Monthly Average Temperature - {CITY_NAME}", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Average Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/monthly_avg_temperature.png", dpi=150)
    plt.close()
    print("Saved: outputs/monthly_avg_temperature.png")

    # 3. Precipitation Distribution
    plt.figure()
    sns.histplot(df["precipitation"], bins=30, color="#2980b9", kde=True)
    plt.title(f"Daily Precipitation Distribution - {CITY_NAME}", fontsize=14, fontweight="bold")
    plt.xlabel("Precipitation (mm)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("outputs/precipitation_distribution.png", dpi=150)
    plt.close()
    print("Saved: outputs/precipitation_distribution.png")

    # 4. Temperature vs Humidity Scatter
    plt.figure()
    sns.scatterplot(data=df, x="temp_mean", y="humidity", hue="precipitation",
                    palette="viridis", size="precipitation", sizes=(20, 200), alpha=0.7)
    plt.title(f"Temperature vs Humidity (colored by Rainfall) - {CITY_NAME}",
              fontsize=14, fontweight="bold")
    plt.xlabel("Mean Temperature (°C)")
    plt.ylabel("Relative Humidity (%)")
    plt.tight_layout()
    plt.savefig("outputs/temp_vs_humidity.png", dpi=150)
    plt.close()
    print("Saved: outputs/temp_vs_humidity.png")

# ====================== MAIN ================================
def main():
    print("Weather Data Analysis Using Python")
    print("-" * 40)

    # Fetch data
    df = fetch_weather_data(LATITUDE, LONGITUDE, DAYS)

    # Save raw data
    data_path = "data/weather_data.csv"
    df.to_csv(data_path, index=False)
    print(f"Raw data saved to: {data_path}")

    # Analyze
    summary = analyze_data(df)

    # Save summary
    with open("outputs/summary.txt", "w") as f:
        f.write(f"Weather Analysis Summary - {CITY_NAME}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")
    print("Saved: outputs/summary.txt")

    # Create plots
    print("\nGenerating visualizations...")
    create_visualizations(df)

    print("\nAnalysis complete! Check the 'outputs/' folder for results.")

if __name__ == "__main__":
    main()
