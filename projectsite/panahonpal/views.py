from django.shortcuts import render
import requests

def index(request):
    weather_data = None
    error = None
    api_key = "11fd8f356ed74979bd9193958250410"
    city = None

    # Manual search
    if request.method == "POST":
        city = request.POST.get("city")

    # Auto-detect on first load
    if not city:
        try:
            ip_response = requests.get("https://ipapi.co/json/", timeout=5)
            ip_data = ip_response.json()
            city = ip_data.get("city", "Manila")  # default fallback
        except requests.RequestException:
            city = "Manila"

    # Fetch weather data from WeatherAPI
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "error" in data:
            error = data["error"]["message"]
        else:
            current = data['current']
            location = data['location']

            weather_data = {
                "city": f"{location['name']}, {location['country']}",
                "temperature": current['temp_c'],
                "humidity": current['humidity'],
                "wind_speed": current['wind_kph'],
                "wind_dir": current['wind_dir'],
                "condition": current['condition']['text'],
                "icon": current['condition']['icon'],
                "feelslike": current['feelslike_c']
            }
    except requests.RequestException:
        error = "Unable to connect to WeatherAPI."

    return render(request, "weather.html", {
        "weather_data": weather_data,
        "error": error
    })
