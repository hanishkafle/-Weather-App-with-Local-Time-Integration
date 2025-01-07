from django.shortcuts import render
import requests
from .models import Profile

def home(request):
    # Get city name from user input, default to 'Nepal'
    city = request.POST.get('city', 'Nepal')

    # OpenWeatherMap API endpoint and parameters
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {'q': city, 'appid': '0522bc2421a154de395ab7fa497a87dd', 'units': 'metric'}

    # Fetch weather data
    weather_response = requests.get(weather_url, params=weather_params)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
    else:
        description = "City not found"
        icon = None
        temp = None

    # Fetch local time based on the city
    local_time = get_local_time(city)

    # Fetch profile data from the database (optional)
    profile_p = Profile.objects.all()

    # Pass data to the template
    return render(request, "index.html", {
        'description': description,
        'icon': icon,
        'temp': temp,
        'city': city,
        'local_time': local_time,
        'profile_p': profile_p,
    })

def get_local_time(country_name):
    # Simple mapping of countries to time zones
    timezones = {
        "Nepal": "Asia/Kathmandu",
        "USA": "America/New_York",
    }
    timezone = timezones.get(country_name, "UTC")  # Default to UTC if not found
    time_api_url = f"http://worldtimeapi.org/api/timezone/{timezone}"

    try:
        time_response = requests.get(time_api_url)
        if time_response.status_code == 200:
            time_data = time_response.json()
            return time_data['datetime']
        else:
            return "Error: Unable to fetch time"
    except Exception:
        return "Error: Unable to connect to the time API"
