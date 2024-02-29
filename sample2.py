from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel

app = FastAPI()

class WeatherInfo(BaseModel):
    condition: str
    temp: str
    feelslike: str

@app.get("/weather/{city}")
async def read_item(city: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://wttr.in/{city}?format=j1")

    soup = BeautifulSoup(r.text, 'lxml')
    weather_data = {
            "condition": soup.find