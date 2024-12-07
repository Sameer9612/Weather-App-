from django.shortcuts import render
import requests
import datetime

def weathers(request):
    city = request.POST.get('city', 'Delhi')  # Default to 'Delhi' if no city is provided

    # OpenWeatherMap API URL and your API Key
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=c1fef141aadae11abe5ba8ed9d1cee20'
    PARAMS = {'units': 'metric'}

    try:
        # Make a request to the OpenWeather API
        response = requests.get(url, params=PARAMS)
        data = response.json()

        # Check if the API returned a valid response
        if response.status_code == 200:
            # Extract weather data
            description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temp = data['main']['temp']
            day = datetime.date.today()
            
            return render(request, 'weather.html', {
                'description': description, 
                'icon': icon, 
                'temp': temp,
                'day': day,
                'city': city
            })
        else:
            # If the response status code is not 200, it means an error occurred
            error_message = data.get('message', 'Unable to fetch weather data. Please try again later.')
            return render(request, 'weather.html', {'error': error_message, 'city': city})

    except requests.exceptions.RequestException as e:
        # Catch any errors related to the request (network issues, invalid URL, etc.)
        return render(request, 'weather.html', {'error': f'Error fetching data: {str(e)}', 'city': city})

