from django.shortcuts import render
import requests

def index(request):
    weather_data = None
    error = None

    api_key = "11fd8f356ed74979bd9193958250410"
    city = None

    # 1️⃣ If user searches manually
    if request.method == "POST":
        city = request.POST.get("city")

    # 2️⃣ If user visits the site (no city yet) — auto detect via IP
    if not city:
        try:
            ip_response = requests.get("https://ipapi.co/json/", timeout=5)
            ip_data = ip_response.json()
            city = ip_data.get("city", "Manila")  # default fallback
        except requests.RequestException:
            city = "Manila"  # fallback if IP lookup fails

    # 3️⃣ Fetch weather data for city (manual or detected)
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "error" in data:
            error = data["error"]["message"]
        else:
            weather_data = {
                "city": f"{data['location']['name']}, {data['location']['country']}",
                "temperature": data['current']['temp_c'],
                "condition": data['current']['condition']['text'],
                "icon": data['current']['condition']['icon'],
                "humidity": data['current']['humidity'],
                "wind": data['current']['wind_kph'],
            }
    except requests.RequestException:
        error = "Unable to connect to WeatherAPI."

    return render(request, "weather.html", {"weather_data": weather_data, "error": error})
