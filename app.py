import streamlit as st
import requests

st.set_page_config(page_title="Weather Station", page_icon="🌦️")

st.title("🌦️ My Personal Weather Station")

# Step 1: Manual Input (More reliable for web apps!)
city = st.text_input("Enter your city name:", "Naaldwijk")

def get_weather(city_name):
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91"
    
    try:
        # Step 2: Fetch Weather for the typed city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("cod") == 401:
            st.warning("⚠️ API Key is still activating. Try again in a bit!")
        elif data.get("cod") == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            
            # Big beautiful display
            st.subheader(f"Current weather in {city_name}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{round(temp)}°C")
            col2.metric("Condition", desc)
            col3.metric("Humidity", f"{humidity}%")
            
            st.success("Fetched live data!")
        else:
            st.error(f"City not found. Check the spelling!")

    except Exception as e:
        st.error(f"System Error: {e}")

if city:
    get_weather(city)

st.divider()
st.caption("Built with Python by Nuri | immanuelnotkant")
