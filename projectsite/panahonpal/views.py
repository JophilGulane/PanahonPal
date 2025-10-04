
import requests
from django.shortcuts import render
from django.http import JsonResponse
import datetime

def index(request):
    api_key = "11fd8f356ed74979bd9193958250410"
    city = request.GET.get("city")

    # Default: Manila if location not given
    if not city:
        city = "Manila"

    # Forecast endpoint: 7 days + hourly
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7&aqi=no&alerts=no"
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        return render(request, "weather.html", {"error": "City not found."})

    current = data["current"]
    location = data["location"]
    forecast_days = data["forecast"]["forecastday"]

    # Hourly forecast for today
    hourly_forecast = forecast_days[0]["hour"]
    now_hour = datetime.datetime.now().hour
    next_hours = hourly_forecast[now_hour:now_hour+12]  # next 12 hours

    context = {
        "city": location["name"],
        "region": location["region"],
        "country": location["country"],
        "temp_c": current["temp_c"],
        "condition": current["condition"]["text"],
        "icon": current["condition"]["icon"],
        "humidity": current["humidity"],
        "wind_kph": current["wind_kph"],
        "wind_dir": current["wind_dir"],
        "forecast_days": forecast_days,
        "hourly_forecast": next_hours,
    }

    return render(request, "weather.html", context)
