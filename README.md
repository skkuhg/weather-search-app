# Weather Search App

A simple weather search application that uses the Tavily API to get current weather conditions for any city worldwide.

## Features

- 🌍 Search weather for any global city
- 🌡️ Display temperature, weather conditions, humidity, and wind speed
- 🔄 Temperature unit toggle (°C/°F)
- ⚡ Quick search buttons for popular cities
- 📱 Responsive design
- 🔄 Loading indicators
- ❌ User-friendly error handling
- 🎨 Clean, minimal UI

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/skkuhg/weather-search-app.git
   cd weather-search-app
   ```

2. **Install required dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure your API key:**
   - Copy `.env.example` to `.env`
   - Add your Tavily API key to the `.env` file:
     ```
     TAVILY_API_KEY=your_actual_tavily_api_key_here
     ```

4. **Run the application:**
   ```powershell
   python app.py
   ```

5. **Open your web browser and go to:**
   ```
   http://localhost:8000
   ```

## How to Use

1. **Enter a city name** in the search field (e.g., "London", "New York", "Tokyo")
2. **Select temperature unit** (°C or °F)
3. **Click "Search Weather"** or press Enter
4. **View the weather results** including:
   - Temperature
   - Weather condition
   - Humidity
   - Wind speed
5. **Use quick search buttons** for popular cities

## API Configuration

The app uses the Tavily search API. You need to:

1. Get a Tavily API key from [Tavily](https://tavily.com/)
2. Copy `.env.example` to `.env`
3. Add your API key to the `.env` file:
   ```
   TAVILY_API_KEY=your_actual_api_key_here
   ```

**Important**: Never commit your actual API key to version control. The `.env` file is ignored by git for security.

## Project Structure

```
weather-app/
├── app.py              # FastAPI backend server
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── static/
    ├── index.html     # Main HTML page
    ├── style.css      # Styling
    └── script.js      # Frontend JavaScript
```

## Technical Details

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **API**: Tavily Search API
- **Features**: 
  - Regex-based weather data extraction
  - Async HTTP requests
  - Error handling and validation
  - Responsive design

## Troubleshooting

- **Port already in use**: If port 8000 is busy, the app will show an error. Stop any other applications using port 8000 or modify the port in `app.py`
- **API errors**: If weather data cannot be found, try different city names or check your internet connection
- **Installation issues**: Make sure you have Python 3.7+ and pip installed correctly

## License

This project is open source and available under the MIT License.