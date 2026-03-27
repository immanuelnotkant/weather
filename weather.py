import requests


def get_weather_magic():
    # 1. Your API Key
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91"

    try:
        # 2. Automatically find where the user is
        geo_data = requests.get("http://ip-api.com/json/").json()
        city = geo_data.get('city', 'London')  # Default to London if it fails
        country = geo_data.get('countryCode', 'GB')

        # 3. Fetch the weather
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"
        response = requests.get(weather_url)

        # This checks if the API key is active yet!
        if response.status_code == 401:
            print("❌ Your API key isn't active yet. Wait about 30-60 minutes!")
            return

        data = response.json()

        # 4. Extract the fun stuff
        temp = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        weather_desc = data['weather'][0]['description'].capitalize()

        print("-" * 30)
        print(f"📍 Location detected: {city}, {country}")
        print(f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)")
        print(f"☁️ Condition: {weather_desc}")
        print("-" * 30)

        if temp < 10:
            print("Pro-tip: It's cold! Tell your friends to bring a coat.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    get_weather_magic()
