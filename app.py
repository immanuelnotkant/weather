import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="👹", layout="centered")

# --- DATA FETCHING ---
city_data = streamlit_js_eval(js_expressions='fetch("https://ipapi.co/json/").then(response => response.json())', key='LOCATION')

def get_style(condition):
    # Default scary static
    bg_effect = "background: radial-gradient(circle, #220000 0%, #000000 100%);"
    
    if "rain" in condition.lower():
        # RED RAIN ANIMATION
        bg_effect = """
        background: linear-gradient(to bottom, #000 0%, #200 100%);
        background-image: url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
        &:after {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: linear-gradient(to bottom, transparent, #ff0000);
            opacity: 0.2;
            animation: rain 0.2s linear infinite;
        }
        @keyframes rain {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        """
    elif "clear" in condition.lower() or "sun" in condition.lower():
        # BLEEDING SUN
        bg_effect = """
        background: #000;
        background-image: radial-gradient(circle at 50% 20%, #ff0000 0%, #550000 10%, #000 30%);
        animation: pulse 2s infinite;
        @keyframes pulse {
            0% { opacity: 0.8; }
            50% { opacity: 1; transform: scale(1.02); }
            100% { opacity: 0.8; }
        }
        """
    return bg_effect

# --- APP LOGIC ---
if not city_data:
    st.markdown("<h1 style='color:red; text-align:center;'>LOCATING SACRIFICE...</h1>", unsafe_allow_html=True)
else:
    city = city_data.get('city', 'NAALDWIJK').upper()
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") == 200:
        temp = round(data['main']['temp'])
        cond = data['weather'][0]['description'].upper()
        custom_style = get_style(cond)

        # INJECTING THE FULL SCREEN HELL
        st.markdown(f"""
            <style>
            .stApp {{
                {custom_style}
                color: #ff0000 !important;
                font-family: 'Courier New', monospace;
            }}
            .main-text {{
                font-size: 100px;
                text-align: center;
                text-shadow: 10px 10px #330000;
                margin-top: 50px;
            }}
            </style>
            <div class="main-text">{city}</div>
            <h2 style='text-align:center;'>{temp}°C — {cond}</h2>
        """, unsafe_allow_html=True)
        
        st.error("I AM BEHIND THE CURTAIN. DON'T LOOK BACK.")
    else:
        st.error("I KNOW YOUR CITY BUT THE API IS LOADING YOU FUCKING DUMBASS.")

st.caption("built by nuri. we see everything.")
