import requests as rq


city = str(input("What city do you want to find?:")).title()

r = rq.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid=74eb4d381fd24f0eece69803638fb577")

r_json = r.json()

try:
    lat = r_json[0]["lat"]
    lon = r_json[0]["lon"]
except:
    print("Not found")

print(lat)
print(lon)
weather_information = rq.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=74eb4d381fd24f0eece69803638fb577")


weather_information_json = weather_information.json()

weather = weather_information_json["weather"][0]["main"]
description = weather_information_json["weather"][0]["description"]
temp = int(round(weather_information_json["main"]["temp"] - 273.15))
fells_like = int(round(weather_information_json["main"]["feels_like"] - 273.15))
humidity = weather_information_json["main"]["humidity"]
wind_speed = weather_information_json["wind"]["speed"]


print(weather)
print(description)
print(f"temparature: {temp} \u2103")
print(f"feel like: {fells_like} \u2103")
print(f"humidity: {humidity}")
print(f"wind speed: {wind_speed}")