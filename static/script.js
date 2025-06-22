class WeatherApp {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
    }

    initializeElements() {
        this.cityInput = document.getElementById('cityInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.weatherResult = document.getElementById('weatherResult');
        this.errorMessage = document.getElementById('errorMessage');
        
        // Weather result elements
        this.cityName = document.getElementById('cityName');
        this.weatherIcon = document.getElementById('weatherIcon');
        this.temperature = document.getElementById('temperature');
        this.description = document.getElementById('description');
        this.humidity = document.getElementById('humidity');
        this.windSpeed = document.getElementById('windSpeed');
        this.errorText = document.getElementById('errorText');
        
        // Unit radio buttons
        this.unitRadios = document.querySelectorAll('input[name="unit"]');
        this.cityButtons = document.querySelectorAll('.city-btn');
    }

    attachEventListeners() {
        // Search button click
        this.searchBtn.addEventListener('click', () => this.handleSearch());
        
        // Enter key in input field
        this.cityInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleSearch();
            }
        });
        
        // Quick city buttons
        this.cityButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const city = e.target.getAttribute('data-city');
                this.cityInput.value = city;
                this.handleSearch();
            });
        });
    }

    async handleSearch() {
        const city = this.cityInput.value.trim();
        if (!city) {
            this.showError('Please enter a city name');
            return;
        }

        const selectedUnit = document.querySelector('input[name="unit"]:checked').value;
        
        this.showLoading();
        this.hideResults();
        this.hideError();

        try {
            const response = await fetch('/api/weather', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    city: city,
                    unit: selectedUnit
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            this.hideLoading();

            if (data.success) {
                this.showWeatherResult(data);
            } else {
                this.showError(data.error || 'Unable to fetch weather data');
            }
        } catch (error) {
            this.hideLoading();
            console.error('Error fetching weather:', error);
            this.showError('Failed to fetch weather data. Please check your connection and try again.');
        }
    }

    showLoading() {
        this.loadingIndicator.classList.remove('hidden');
        this.searchBtn.disabled = true;
        this.searchBtn.textContent = 'Searching...';
    }

    hideLoading() {
        this.loadingIndicator.classList.add('hidden');
        this.searchBtn.disabled = false;
        this.searchBtn.textContent = 'Search Weather';
    }

    showWeatherResult(data) {
        this.cityName.textContent = data.city;
        this.temperature.textContent = data.temperature || 'N/A';
        this.description.textContent = data.description || 'N/A';
        this.humidity.textContent = data.humidity || 'N/A';
        this.windSpeed.textContent = data.wind_speed || 'N/A';
        
        // Set weather icon based on description
        this.weatherIcon.textContent = this.getWeatherIcon(data.description);
        
        this.weatherResult.classList.remove('hidden');
    }

    hideResults() {
        this.weatherResult.classList.add('hidden');
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorMessage.classList.remove('hidden');
    }

    hideError() {
        this.errorMessage.classList.add('hidden');
    }

    getWeatherIcon(description) {
        if (!description) return '🌤️';
        
        const desc = description.toLowerCase();
        
        if (desc.includes('sunny') || desc.includes('clear')) return '☀️';
        if (desc.includes('cloudy') || desc.includes('overcast')) return '☁️';
        if (desc.includes('partly')) return '⛅';
        if (desc.includes('rain') || desc.includes('drizzle')) return '🌧️';
        if (desc.includes('thunderstorm') || desc.includes('storm')) return '⛈️';
        if (desc.includes('snow')) return '🌨️';
        if (desc.includes('fog')) return '🌫️';
        if (desc.includes('wind')) return '💨';
        
        return '🌤️'; // Default icon
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WeatherApp();
});