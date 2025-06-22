from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import json
import re
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Weather Search App")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Tavily API configuration
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_API_URL = "https://api.tavily.com/search"

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY environment variable is required")

class WeatherRequest(BaseModel):
    city: str
    unit: str = "celsius"  # celsius or fahrenheit

class WeatherResponse(BaseModel):
    city: str
    temperature: Optional[str] = None
    description: Optional[str] = None
    humidity: Optional[str] = None
    wind_speed: Optional[str] = None
    success: bool = True
    error: Optional[str] = None

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

def extract_weather_info(content: str, city: str) -> dict:
    """Extract weather information from search results"""
    weather_info = {
        "temperature": None,
        "description": None,
        "humidity": None,
        "wind_speed": None
    }
    
    # Convert to lowercase for case-insensitive matching
    content_lower = content.lower()
    
    # Temperature patterns
    temp_patterns = [
        r'(\d+)°?\s*[cf]',
        r'temperature:?\s*(\d+)°?\s*[cf]',
        r'(\d+)\s*degrees?',
        r'temp:?\s*(\d+)°?\s*[cf]'
    ]
    
    for pattern in temp_patterns:
        match = re.search(pattern, content_lower)
        if match:
            weather_info["temperature"] = f"{match.group(1)}°"
            break
    
    # Weather description patterns
    weather_conditions = [
        'sunny', 'cloudy', 'rainy', 'stormy', 'snowy', 'foggy', 'windy',
        'partly cloudy', 'overcast', 'clear', 'thunderstorms', 'drizzle',
        'fair', 'partly sunny', 'mostly cloudy', 'light rain', 'heavy rain'
    ]
    
    for condition in weather_conditions:
        if condition in content_lower:
            weather_info["description"] = condition.title()
            break
    
    # Humidity patterns
    humidity_patterns = [
        r'humidity:?\s*(\d+)%?',
        r'(\d+)%\s*humidity'
    ]
    
    for pattern in humidity_patterns:
        match = re.search(pattern, content_lower)
        if match:
            weather_info["humidity"] = f"{match.group(1)}%"
            break
    
    # Wind speed patterns
    wind_patterns = [
        r'wind:?\s*(\d+)\s*(?:mph|km/h|kph)',
        r'wind speed:?\s*(\d+)\s*(?:mph|km/h|kph)',
        r'(\d+)\s*(?:mph|km/h|kph)\s*wind'
    ]
    
    for pattern in wind_patterns:
        match = re.search(pattern, content_lower)
        if match:
            weather_info["wind_speed"] = f"{match.group(1)} mph"
            break
    
    return weather_info

@app.post("/api/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest):
    try:
        # Prepare search query
        unit_text = "Celsius" if request.unit == "celsius" else "Fahrenheit"
        query = f"current weather in {request.city} temperature humidity wind speed {unit_text}"
        
        # Make request to Tavily API
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "include_answer": True,
            "include_raw_content": False,
            "max_results": 5
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(TAVILY_API_URL, json=payload)
            response.raise_for_status()
            
            search_results = response.json()
            
            # Extract weather information from results
            weather_data = {
                "temperature": None,
                "description": None,
                "humidity": None,
                "wind_speed": None
            }
            
            # Check if there's a direct answer
            if search_results.get("answer"):
                answer_info = extract_weather_info(search_results["answer"], request.city)
                for key, value in answer_info.items():
                    if value and not weather_data[key]:
                        weather_data[key] = value
            
            # Check search results
            if search_results.get("results"):
                for result in search_results["results"]:
                    content = result.get("content", "")
                    title = result.get("title", "")
                    combined_content = f"{title} {content}"
                    
                    result_info = extract_weather_info(combined_content, request.city)
                    for key, value in result_info.items():
                        if value and not weather_data[key]:
                            weather_data[key] = value
            
            # Check if we got any weather data
            if not any(weather_data.values()):
                return WeatherResponse(
                    city=request.city,
                    success=False,
                    error=f"Weather information not found for {request.city}. Please check the city name and try again."
                )
            
            return WeatherResponse(
                city=request.city,
                temperature=weather_data["temperature"],
                description=weather_data["description"],
                humidity=weather_data["humidity"],
                wind_speed=weather_data["wind_speed"],
                success=True
            )
            
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"Search API error: {str(e)}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=500, detail="Request timeout. Please try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)