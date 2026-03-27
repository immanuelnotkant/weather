import streamlit as st
import requests
import random

# Setting the vibe
st.set_page_config(page_title="EYE_OF_RA", page_icon="👁️")

# Schizo/Glitch Styling
st.markdown("""
    <style>
    .reportview-container { background: #000000; }
    .glitch {
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        text-shadow: 2px 2px #ff0000;
        animation: shake 0.2s infinite;
        font-size: 50px;
        text-align: center;
    }
    @keyframes shake {
        0% { transform: translate(2px, 2px); }
        50% { transform: translate(-2px, -2px); }
        100% { transform: translate(1px, -1px); }
    }
    </style>
    """, unsafe_allow_html=True)

def get_visitor_city():
    try:
        # Poking the visitor's IP directly
        res = requests.get('https://ipapi.co/json/', timeout=5)
        return res.json().get('city', 'THE VOID').upper()
    except:
        return "NOWHERE"

# Automatically trigger the hunt
city = get_visitor_city()

def get_weather(city_name):
    # Your verified API Key
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") == 200:
            temp = round(data['main']['temp'])
            desc = data['weather'][0]['description'].upper()
            
            # THE REVEAL
            st.markdown(f'<p class="glitch">{city_name}</p>', unsafe_allow_html=True)
            st.write(f"### {temp}°C | {desc}")
            
            # Schizo static
            st.info(random.choice([
                "THE CODE IS UNDER YOUR SKIN.",
                "STOP BREATHING SO LOUD.",
                "I CAN SEE YOU THROUGH THE SCREEN.",
                "01001000 01000101 01001100 01010000"
            ]))
            
        elif data.get("cod") == 401:
            # THE SPECIFIC ERROR MESSAGE YOU WANTED
            st.markdown(f'<p class="glitch">{city_name}</p>', unsafe_allow_html=True)
            st.error("I KNOW YOUR CITY BUT THE API IS LOADING YOU FUCKING DUMBASS. REFRESH IN 15 MINS.")
        else:
            st.error("SYSTEM COLLAPSE. REFRESH OR DIE.")
            
    except:
        st.error("REALITY.EXE HAS STOPPED WORKING.")

get_weather(city)

st.divider()
st.caption("nuri built this f'{(or as they call me nuri)}' built this by python  march 2026")
