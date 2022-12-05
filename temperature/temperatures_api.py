import requests, os
url = f"https://api.weatherapi.com/v1/current.json?key={os.environ['WEATHER_KEY']}&q=Berlin&aqi=no"
url_int = "http://192.168.0.10/temp"

def get_berlin_temperature():
    response = requests.request("GET", url)
    response = response.json()
    return response['current']['temp_c']

def get_internal_temp():
    response = requests.request("GET", url_int)
    return response.text