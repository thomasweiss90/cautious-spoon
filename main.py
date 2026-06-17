import os
import requests
import asyncio
from datetime import datetime, timedelta
from telegram import Bot

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
WEATHER_KEY = os.environ["WEATHER_API_KEY"]

SPOTS = {
    "leipzig": {"name": "Leipzig", "pegel": "501420", "lat": 51.33, "lon": 12.37},
    "bennewitz": {"name": "Bennewitz", "pegel": "503210", "lat": 51.37, "lon": 12.72},
    "torgau": {"name": "Torgau", "pegel": "500410", "lat": 51.56, "lon": 13.02},
}

def classify_pegel(value):
    if value is None:
        return "keine Daten"
    if value < 150:
        return "niedrig"
    if value < 300:
        return "normal"
    return "hoch"

def classify_pressure(value):
    if value is None:
        return "keine Daten"
    if value < 1010:
        return "niedrig"
    if value <= 1020:
        return "normal"
    return "hoch"

def classify_rain(value):
    if value is None:
        return "keine Daten"
    if value == 0:
        return "trocken"
    if value < 2:
        return "leicht"
    if value < 10:
        return "mäßig"
    return "stark"

def get_pegel(station):
    try:
        url = f"https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station}/W/measurements.json"
        data = requests.get(url, params={"start": "P1D"}, timeout=10).json()
        if not data:
            return None

        current = data[-1]["value"]
        trend = current - data[-7]["value"] if len(data) > 6 else 0

        return {
            "current": current,
            "trend": trend,
        }
    except:
        return None

def get_weather(lat, lon):
    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        data = requests.get(
            url,
            params={
                "lat": lat,
                "lon": lon,
                "appid": WEATHER_KEY,
                "units": "metric",
                "lang": "de",
            },
            timeout=10
        ).json()

        if "list" not in data:
            return None

        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        day = [            x for x in data["list"]
            if tomorrow in x["dt_txt"] and 6 <= int(x["dt_txt"]) <= 18
        ]

        if not day:
            return None

        temps = [x["main"]["temp"] for x in day]
        rain = sum(x.get("rain", {}).get("3h", 0) for x in day)
        wind = max(x["wind"]["speed"] for x in day)
        pressure = day["main"]["pressure"]

        return {
            "temp_min": min(temps),
            "temp_max": max(temps),
            "rain_mm": rain,
            "wind_max": wind,
            "pressure": pressure,
        }
    except:
        return None

async def main():
    bot = Bot(TOKEN)
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")

    msg = f"Angel-Check für morgen ({tomorrow})\n\n"

    for spot in SPOTS.values():
        pegel = get_pegel(spot["pegel"])
        weather = get_weather(spot["lat"], spot["lon"])

        msg += f"{spot['name']}\n"

        if pegel:
            trend_text = "steigend" if pegel["trend"] > 0 else "fallend" if pegel["trend"] < 0 else "gleich"
            msg += f"Wasserstand: {pegel['current']} cm ({classify_pegel(pegel['current'])})\n"
            msg += f"Trend: {trend_text} ({pegel['trend']:+.0f} cm/24h)\n"
        else:
            msg += "Wasserstand: keine Daten\n"
            msg += "Trend: keine Daten\n"

        if weather:
            msg += f"Luftdruck: {weather['pressure']} hPa ({classify_pressure(weather['pressure'])})\n"
            msg += (
                f"Wetter: {weather['temp_min']:.0f}-{weather['temp_max']:.0f} °C, "
                f"Regen {weather['rain_mm']:.1f} mm ({classify_rain(weather['rain_mm'])}), "
                f"Wind {weather['wind_max']:.0f} m/s\n"
            )
        else:
            msg += "Luftdruck: keine Daten\n"
            msg += "Wetter: keine Daten\n"

        msg += "\n"

    await bot.send_message(chat_id=CHAT_ID, text=msg)

if __name__ == "__main__":
    asyncio.run(main())
