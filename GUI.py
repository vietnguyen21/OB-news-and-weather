
import PySimpleGUI as sg
import requests as rq
import cv2

frame = cv2.imread("forecast.jpg")
frame = cv2.resize(frame,(200,75))
rain = cv2.imread("rain.png")
rain = cv2.resize(rain,(75,75))
sun = cv2.imread("sun.png")
sun = cv2.resize(sun,(75,75))
cloud = cv2.imread("cloud.png")
cloud = cv2.resize(cloud,(75,75))

sg.theme('DarkTeal3')

world_news = rq.get("https://api.nytimes.com/svc/topstories/v2/world.json?api-key=OcxS60gEJGK534n3jLYRKqb4OPyfo3SY")
sport_news = rq.get("https://api.nytimes.com/svc/topstories/v2/sports.json?api-key=OcxS60gEJGK534n3jLYRKqb4OPyfo3SY")
business = rq.get("https://api.nytimes.com/svc/topstories/v2/business.json?api-key=OcxS60gEJGK534n3jLYRKqb4OPyfo3SY")
home_news = rq.get("https://api.nytimes.com/svc/topstories/v2/home.json?api-key=OcxS60gEJGK534n3jLYRKqb4OPyfo3SY")

news = []
world_json = list(dict(world_news.json())['results'])
sport_json = list(dict(sport_news.json())['results'])
business_json = list(dict(business.json())['results'])
home_json = list(dict(home_news.json())['results'])


for i in range(2):
    news.append(world_json[i])
    news.append(sport_json[i])
    news.append(business_json[i])
    news.append(home_json[i])

text = []
for new in news:
    text.append(f"Title: {new['title']}\n")
    text.append(f"Description: {new['abstract']}\n")
    text.append(f"URL: {new['url']}\n\n")
    text.append([])

#LAYOUT
file_list_column = [
    [sg.Image('forecast.png',size=(100,100))],
    [sg.Text("OB.WEATHER")],
    [sg.Input(size=(50, 10), key="city")],
    [sg.Button("Search",size=(20,2), key="search")],
    [sg.Text(size=(50, 1), key="-weather-")],
    [sg.Text(size=(50, 1), key="-description-")],
    [sg.Text(size=(50, 1), key="-temp-")],
    [sg.Text(size=(50, 1), key="-feels_like-")],
    [sg.Text(size=(50, 1), key="-humidity-")],
    [sg.Text(size=(50, 1), key="-wind_speed-")],
    [sg.Image(frame, key="-FORECAST-")],
]
# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("NEWSSSSSS")],
    [
        sg.Listbox(
            values=text, enable_events=True, size=(100,40), key="-FILE LIST-"
        )
    ],
]
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]


window = sg.Window("OB.Weather", layout,size=(1000,500))

while True:
    event, values = window.read()
    if event == "Close" or event == sg.WIN_CLOSED:
        break

    if event == "search":
        city = values["city"].title()

        api_key = "74eb4d381fd24f0eece69803638fb577"
        try:
            r = rq.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}")
            r.raise_for_status()
            r_json = r.json()
            lat = r_json[0]["lat"]
            lon = r_json[0]["lon"]
            try:
                weather_information = rq.get(
                    f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
                )
                weather_information.raise_for_status()

                weather_information_json = weather_information.json()

                weather = weather_information_json["weather"][0]["main"]
                description = weather_information_json["weather"][0]["description"]
                temp = int(round(weather_information_json["main"]["temp"] - 273.15))
                feels_like = int(round(weather_information_json["main"]["feels_like"] - 273.15))
                humidity = weather_information_json["main"]["humidity"]
                wind_speed = weather_information_json["wind"]["speed"]

                window["-weather-"].update(f"Weather: {weather}")
                window["-description-"].update(f"Description: {description}")
                window["-temp-"].update(f"Temp: {temp}°C")
                window["-feels_like-"].update(f"Feels like: {feels_like}°C")
                window["-humidity-"].update(f"Humidity: {humidity}%")
                window["-wind_speed-"].update(f"Wind speed: {wind_speed} m/s")
                if "Clouds" == weather:
                    imgbytes = cv2.imencode(".png", cloud)[1].tobytes()
                    window["-FORECAST-"].update(data=imgbytes)
                elif "rain" in weather:
                    imgbytes = cv2.imencode(".png", rain)[1].tobytes()
                    window["-FORECAST-"].update(data=imgbytes)
                elif "Clear" == weather:
                    imgbytes = cv2.imencode(".png", sun)[1].tobytes()
                    window["-FORECAST-"].update(data=imgbytes)
                else:
                    imgbytes = cv2.imencode(".png", frame)[1].tobytes()
                    window["-FORECAST-"].update(data=imgbytes)

                

        
            except rq.exceptions.RequestException as e:
                print(f"Error retrieving weather data: {e}")
                window["-weather-"].update("Error retrieving weather data")

        except rq.exceptions.RequestException as e:
            print(f"Error finding location: {e}")
            window["-weather-"].update("Error finding location")

window.close()
