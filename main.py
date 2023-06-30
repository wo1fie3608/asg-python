import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import Response


API_KEY = "" # THE API_KEY TODO: PLEASE ENTER YOUR API KEY
WEATHER_API_URL = "https://weatherapi-com.p.rapidapi.com/current.json"

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class WeatherResponse(BaseModel):
    Weather: str
    Latitude: str
    Longitude: str
    City: str


class Data(BaseModel):
    city: str 
    output_format: str

@app.post("/getCurrentWeather")
def get_current_weather(data : Data):
    print(data)
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    params = {
        "q": data.city,
    }

    try:
        response = requests.get(WEATHER_API_URL, headers=headers, params=params)
        response.raise_for_status()
        weather_data = response.json()
        print(response.json())
        weather = WeatherResponse(
            Weather=str(weather_data["current"]["temp_c"]) + " C",
            Latitude=weather_data["location"]["lat"],
            Longitude=weather_data["location"]["lon"],
            City=weather_data["location"]["name"] + " "+ weather_data["location"]["country"],
        )

        if data.output_format == "json":
            return weather.dict()
        elif data.output_format == "xml":
            xml_body = f"""<?xml version="1.0" encoding="UTF-8" ?>
            <root>
                <Temperature>{weather.Weather}</Temperature>
                <City>{weather.City}</City>
                <Latitude>{weather.Latitude}</Latitude>
                <Longitude>{weather.Longitude}</Longitude>
            </root>
            """
            return Response(content=xml_body, media_type="application/xml")
        else:
            raise HTTPException(
                status_code=400, detail="Invalid output_format. Must be 'json' or 'xml'."
            )

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


