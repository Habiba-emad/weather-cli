import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherReport:
    """Stores the parsed weather data for one city."""

    def __init__(self, city, country, temp, feels_like,
                 humidity, wind_speed, description):
        self.city = city
        self.country = country
        self.temp = temp
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.description = description

    @classmethod
    def from_api(cls, data):
        return cls(
            city=data["name"],
            country=data["sys"]["country"],
            temp=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"],
            description=data["weather"][0]["description"].title(),
        )

    def print_summary(self):
        line = "=" * 36
        print(line)
        print(f" Weather in {self.city}, {self.country}")
        print(line)
        print(f" Condition   : {self.description}")
        print(f" Temperature : {self.temp:.1f} °C")
        print(f" Feels like  : {self.feels_like:.1f} °C")
        print(f" Humidity    : {self.humidity}%")
        print(f" Wind speed  : {self.wind_speed} m/s")
        print(line)


def fetch_weather(city):
    if not API_KEY:
        sys.exit("Error: OPENWEATHER_API_KEY not found in .env file.")

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        sys.exit(f"API error {response.status_code}: check the city name or API key.")
    except requests.exceptions.RequestException as err:
        sys.exit(f"Network error: {err}")

    return response.json()


def main():
    city = input("Enter city name (default: Cairo): ").strip() or "Cairo"
    data = fetch_weather(city)
    report = WeatherReport.from_api(data)
    report.print_summary()


if __name__ == "__main__":
    main()