import streamlit as st
import requests

st.set_page_config(page_title="Weather Station", page_icon="🌦️")

st.title("🌦️ My Personal Weather Station")
st.write("Detecting your location and fetching the sky...")

def get_weather():
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91"
    
    try:
        # Step 1: Detect Location
        geo_response = requests.get("http://ip-api.com/json/", timeout=5)
        geo_data = geo_response.json()
        city = geo_data.get('city', 'Naaldwijk')
        
        st.write(f"📍 Detected City: **{city}**")

        # Step 2: Fetch Weather
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        weather_response = requests.get(url, timeout=5)
        data = weather_response.json()

        if data.get("cod") == 401:
            st.warning("⚠️ API Key is still activating. Grab a snack and refresh in 15 mins!")
        elif data.get("cod") == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].capitalize()
            
            # Big beautiful display
            col1, col2 = st.columns(2)
            col1.metric("Temperature", f"{round(temp)}°C")
            col2.metric("Condition", desc)
            
            st.success("Data updated successfully!")
        else:
            st.error(f"Weather API Error: {data.get('message')}")

    except Exception as e:
        st.error(f"System Error: {e}")

get_weather()

# A little credit at the bottom
st.divider()
st.caption("Built with Python by Nuri | immanuelnotkant")
