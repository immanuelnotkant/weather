import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="DO NOT REFRESH", layout="centered")

# --- THE LOCATION GRABBER ---
city_data = streamlit_js_eval(js_expressions='fetch("https://ipapi.co/json/").then(response => response.json())', key='LOCATION')

def get_weather_theme(condition):
    cond = condition.lower()
    
    # Default Fallback
    css = "background: #050000;"
    message = "01010100 01001000 01000101 01011001 00100000 01001100 01001001 01000101"
    
    if "thunder" in cond or "storm" in cond:
        css = """
        background: #000;
        animation: flash 0.2s infinite;
        @keyframes flash {
            0%, 95%, 98% { background-color: #000; }
            96%, 99% { background-color: #fff; }
        }
        """
        message = "THE SKY IS SCREAMING. UNPLUG YOUR ROUTER BEFORE IT HEARS YOU."
        
    elif "rain" in cond or "drizzle" in cond:
        css = """
        background: linear-gradient(to bottom, #000 0%, #200 100%);
        &:after {
            content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(to bottom, transparent, #ff0000);
            opacity: 0.3; animation: rain 0.1s linear infinite;
        }
        @keyframes rain { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
        """
        message = "IT'S RAINING. DON'T DRINK IT. IT TASTES LIKE COPPER."
        
    elif "snow" in cond:
        css = """
        background: #000;
        background-image: radial-gradient(#555 1px, transparent 1px);
        background-size: 20px 20px;
        animation: ash 4s linear infinite;
        @keyframes ash { 0% { background-position: 0 0; } 100% { background-position: 20px 40px; } }
        """
        message = "THAT ISN'T SNOW. IT'S ASH FROM THE INCINERATOR."
        
    elif "clear" in cond or "sun" in cond:
        css = """
        background: #000;
        background-image: radial-gradient(circle at 50% 20%, #ff0000 0%, #400 15%, #000 40%);
        animation: pulse 1.5s infinite;
        @keyframes pulse { 0%, 100% { opacity: 0.8; } 50% { opacity: 1; transform: scale(1.05); } }
        """
        message = "THE SUN IS A DEADLY LASER. DO NOT GO OUTSIDE."
        
    elif "cloud" in cond or "overcast" in cond or "fog" in cond:
        css = """
        background: #050505;
        box-shadow: inset 0 0 150px #000;
        animation: breathe 3s infinite alternate;
        @keyframes breathe { 0% { opacity: 0.7; } 100% { opacity: 1; filter: blur(2px); } }
        """
        message = "THERE IS SOMETHING TALL IN THE FOG. DON'T LOOK UP."
        
    return css, message

# --- APP LOGIC ---
if not city_data:
    # No indentation here either!
    st.markdown("<h1 style='color:red; text-align:center; font-family:Courier;'>TRACING IP...</h1>", unsafe_allow_html=True)
else:
    city = city_data.get('city', 'NOWHERE').upper()
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91" 
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") == 200:
        temp = round(data['main']['temp'])
        cond = data['weather'][0]['description'].upper()
        custom_style, threat_message = get_weather_theme(cond)

        # HTML Block with NO leading spaces so Markdown doesn't think it's code
        html_block = f"""
<style>
.stApp {{
    {custom_style}
    color: #ff0000 !important;
    font-family: 'Courier New', monospace;
}}
.main-text {{
    font-size: 90px;
    text-align: center;
    text-shadow: 5px 5px #330000;
    margin-top: 50px;
    font-weight: bold;
    animation: shake 0.5s infinite;
}}
@keyframes shake {{
    0% {{ transform: translate(1px, 1px); }}
    50% {{ transform: translate(-1px, -1px); }}
    100% {{ transform: translate(1px, -1px); }}
}}
</style>
<div class="main-text">{city}</div>
<h2 style='text-align:center;'>{temp}°C — {cond}</h2>
"""
        st.markdown(html_block, unsafe_allow_html=True)
        st.error(threat_message)
    else:
        st.error("I KNOW YOUR CITY BUT THE API IS LOADING YOU FUCKING DUMBASS.")

st.markdown("---")
st.caption("built by nuri. i see you through your webcam.")
