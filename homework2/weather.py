from collections import defaultdict
import datetime
import requests
import numpy as np
import matplotlib.pyplot as plt
import mpld3
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from dotenv import load_dotenv
import os
from Constants import BASE_URL1, BASE_URL2, HTML_FORM, HTML_TEMPLATE
from fastapi.middleware.cors import CORSMiddleware

load_dotenv("secret.env")
API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "city", "start_date", "end_date", "password"],
)

def get_current_weather(city: str):
    if not city or city.strip() == "":
        error_html = "<h1>Error: City parameter is required</h1><p>Please provide a city name.</p><img src='/problem.png'>"
        return HTMLResponse(content=error_html, status_code=400)
    
    current_weather_url = f"{BASE_URL1}appid={API_KEY}&q={city}"
    response = requests.get(current_weather_url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            error_html = f"<h1>Error: City {city} not found :(</h1><p>{e}</p><img src='/problem.png'>"
            return HTMLResponse(content=error_html, status_code=404)
    return response.json()

def validate_date_range(start_date: str, end_date: str):
    try:
        start_datetime = datetime.datetime.fromisoformat(start_date)
        end_datetime = datetime.datetime.fromisoformat(end_date)
        if start_datetime > end_datetime:
            raise ValueError("Start date cannot be later than end date")
        elif start_datetime == end_datetime:
            raise ValueError("Wrong dates range given")
        elif start_datetime > datetime.datetime.now():
            raise ValueError("Start date cannot be in the future")
        elif end_datetime > datetime.datetime.now():
            raise ValueError("End date cannot be in the future")
        
    except ValueError as e:
        error_html = f"<h1>Error: Invalid date format or start date later than end date</h1><p>{e}</p><img src='/problem.png'>"
        return HTMLResponse(content=error_html, status_code=400)

def get_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str):
    validation_response = validate_date_range(start_date, end_date)
    
    if validation_response is not None:
        return validation_response
    
    historical_weather_url = f"{BASE_URL2}latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
    response = requests.get(historical_weather_url)
    response.raise_for_status()
    return response.json()["hourly"]

def calculate_average_temperature(historical_temperatures):
    return np.mean(historical_temperatures)

def generate_daily_temperatures(historical_data):
    times = [datetime.datetime.fromisoformat(time) for time in historical_data["time"]]
    daily_temperatures = defaultdict(list)
    for time, temperature in zip(times, historical_data["temperature_2m"]):
        date = time.date()
        daily_temperatures[date].append(temperature)
    return daily_temperatures

def generate_plot(city, dates, temperatures):
    try:
        plt.figure(figsize=(5, 3))
        plt.plot(dates, temperatures, marker='o', linestyle='-', color='hotpink')
        plt.title(f'Average Daily Temperatures in {city}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.grid(True)
        html_plot = mpld3.fig_to_html(plt.gcf())
        plt.clf()
        return html_plot
    
    except:
        raise Exception("Internal server had problem while creating plot")

def calculate_average_daily_temperatures(daily_temperatures):
    average_daily_temperatures = {date: sum(temps) / len(temps) for date, temps in daily_temperatures.items()}
    dates = list(average_daily_temperatures.keys())
    temperatures = list(average_daily_temperatures.values())
    return dates, temperatures

@app.get("/", response_class=HTMLResponse)
async def weather_form():
    return HTML_FORM

@app.post("/weather", response_class=HTMLResponse)
async def get_weather(city: str = Form(None), start_date: str = Form(...), end_date: str = Form(...), password: str = Form(None)):
    if not password or password.strip() == "" or password != PASSWORD:
        error_html = "<h1>Error: Authorization Failed</h1><p>Please provide a valid password.</p><img src='/problem.png'>"
        return HTMLResponse(content=error_html, status_code=401)
    
    try:
        current_data = get_current_weather(city)
        if isinstance(current_data, HTMLResponse):
            return current_data
            
        temperature_current = current_data["main"]["temp"]
        temperature_current_celsius = temperature_current - 273.15
        humidity_current = current_data["main"]["humidity"]
        latitude = current_data["coord"]["lat"]
        longitude = current_data["coord"]["lon"]

        historical_data = get_historical_weather(latitude, longitude, start_date, end_date)
        if isinstance(historical_data, HTMLResponse):
            return historical_data
        
        if not historical_data:
            raise ValueError("No historical weather data found for the provided location")

        average_temperature = calculate_average_temperature(historical_data["temperature_2m"])

        daily_temperatures = generate_daily_temperatures(historical_data)
        if not daily_temperatures:
            raise ValueError("Failed to generate daily temperatures")

        dates, temperatures = calculate_average_daily_temperatures(daily_temperatures)

        html_response = HTML_TEMPLATE.format(
            city=city, 
            temperature_current_celsius=temperature_current_celsius, 
            humidity_current=humidity_current, 
            average_temperature=average_temperature, 
            html_plot=generate_plot(city, dates, temperatures)
            )
        
        return HTMLResponse(content=html_response, status_code=200)
    
    except requests.RequestException as e:
        error_html = f"<h1>External service unavailable :(</h1><p>The external service did not find a response. </p><img src='/problem.png'>"
        return HTMLResponse(content=error_html, status_code=503)
    except KeyError as e:
        error_html = f"<h1>Data not found :(</h1><p>{e}</p><img src='/problem.png'>"
        return HTMLResponse(content=error_html, status_code=404)
    except ValueError as e:
        error_html = f"<h1>Error :(</h1><p>{e}</p><img src='/problem.png'>"
        return HTMLResponse(content=error_html, status_code=404)
    except HTTPException as e:
        error_html = f"<h1>Client error :(</h1><p>{e.detail}</p><img src='/problem.png'>"
        return HTMLResponse(content=error_html, status_code=e.status_code)
    except Exception as e:
        error_html = f"<h1>Internal server error :(</h1><p>{str(e)}</p><img src='/problem.png'>"
        return HTMLResponse(content=error_html, status_code=500)

@app.get("/problem.png")
async def problem_image():
    return FileResponse("problem.png", media_type="image/png")