import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="👹", layout="centered")

# The Scary Styling
st.markdown("""
    <style>
    body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: #ff0000 !important;
    }
    .glitch {
        color: #ff0000;
        font-size: 80px;
        text-align: center;
        text-shadow: 5px 5px #550000;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# THE NEW LOCATION GRABBER
# This asks the browser for the IP info directly
city_data = streamlit_js_eval(js_expressions='fetch("https://ipapi.co/json/").then(response => response.json())', key='LOCATION')

def get_weather(city_json):
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91"
    
    if not city_json:
        st.markdown('<p class="glitch">BREATHING...</p>', unsafe_allow_html=True)
        return

    city = city_json.get('city', 'NAALDWIJK').upper()

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") == 200:
            temp = round(data['main']['temp'])
            st.markdown(f'<p class="glitch">{city}</p>', unsafe_allow_html=True)
            st.write(f"### {temp}°C | {data['weather'][0]['description'].upper()}")
            st.error("I AM BEHIND THE CURTAIN.")
            
        elif data.get("cod") == 401:
            st.markdown(f'<p class="glitch">{city}</p>', unsafe_allow_html=True)
            st.error("I KNOW YOUR CITY BUT THE API IS LOADING YOU FUCKING DUMBASS. REFRESH.")
    except:
        st.write("EYES EYES EYES EYES EYES")

get_weather(city_data)

st.markdown("---")
st.caption("built by nuri. i see you.")
# Creepy footer
st.markdown("---")
st.caption("built by nuri. i see you through the webcam.")
