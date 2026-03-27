import streamlit as st
import requests

st.set_page_config(page_title="Weather Station", page_icon="🌦️")

# --- THE SECRET SAUCE ---
# We use a different service that is better at identifying the visitor, not the server.
def get_visitor_city():
    try:
        # This service specifically looks at the client (your friend)
        res = requests.get('https://ipapi.co/json/')
        data = res.json()
        return data.get('city', 'Naaldwijk')
    except:
        return "Naaldwijk" # Fallback just in case

# --- THE APP ---
st.title("🌦️ My Personal Weather Station")

# It happens automatically in the background
detected_city = get_visitor_city()

def get_weather(city_name):
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") == 200:
        temp = data['main']['temp']
        desc = data['weather'][0]['description'].capitalize()
        
        st.markdown(f"### I see you're in **{city_name}**!")
        
        col1, col2 = st.columns(2)
        col1.metric("Temperature", f"{round(temp)}°C")
        col2.metric("Condition", desc)
        
        st.success("Live data fetched automatically.")
    else:
        # If the API key is still activating, we show this:
        st.warning("📍 Detected your city, but the Weather API is still warming up. Refresh in 10 mins!")

get_weather(detected_city)

st.divider()
st.caption("Built with Python by Nuri | immanuelnotkant")
