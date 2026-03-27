import streamlit as st
import requests
import base64
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="666", layout="centered")

# --- DATA FETCHING ---
city_data = streamlit_js_eval(js_expressions='fetch("https://ipapi.co/json/").then(response => response.json())', key='LOCATION')

# Function to allow the background image to work
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    try:
        bin_str = get_base64(png_file)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.7); /* Darkens the image so you can read text */
            z-index: -1;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except:
        st.markdown("<style>.stApp { background-color: black; }</style>", unsafe_allow_html=True)

# Set the background image (Make sure the filename matches exactly)
set_background('images.jpeg')

# --- HIDDEN AUDIO PLAYER ---
# This plays a creepy atmospheric drone loop
st.markdown(
    """
    <iframe src="https://www.youtube.com/embed/S_73pG8Lp_8?autoplay=1&loop=1&playlist=S_73pG8Lp_8" 
    width="0" height="0" frameborder="0" allow="autoplay"></iframe>
    """,
    unsafe_allow_html=True
)

def get_weather_theme(condition):
    cond = condition.lower()
    if "thunder" in cond or "storm" in cond:
        return "animation: flash 0.1s infinite;", "THE SKY IS SCREAMING. IT WANTS IN."
    elif "rain" in cond:
        return "animation: bleed 0.5s infinite;", "IT'S RAINING BLOOD IN YOUR STREETS."
    elif "clear" in cond or "sun" in cond:
        return "animation: pulse 2s infinite;", "THE EYE IN THE SKY IS WATCHING YOU BLINK."
    return "opacity: 0.9;", "THE FOG IS FULL OF TEETH."

# --- APP LOGIC ---
if not city_data:
    st.markdown("<h1 style='color:red; text-align:center; font-family:Courier;'>PEERING THROUGH THE GLASS...</h1>", unsafe_allow_html=True)
else:
    city = city_data.get('city', 'NOWHERE').upper()
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91" 
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") == 200:
        temp = round(data['main']['temp'])
        cond = data['weather'][0]['description'].upper()
        anim, threat = get_weather_theme(cond)

        html_block = f"""
<style>
.stApp {{
    color: #ff0000 !important;
    font-family: 'Courier New', monospace;
}}
.main-text {{
    font-size: clamp(50px, 10vw, 100px);
    text-align: center;
    text-shadow: 0 0 20px #ff0000;
    margin-top: 20px;
    font-weight: bold;
    {anim}
}}
@keyframes flash {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
@keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.1); }} 100% {{ transform: scale(1); }} }}
</style>
<div class="main-text">{city}</div>
<h2 style='text-align:center; text-shadow: 2px 2px #000;'>{temp}°C — {cond}</h2>
"""
        st.markdown(html_block, unsafe_allow_html=True)
        st.error(threat)
    else:
        st.error("I SEE YOUR FACE BUT THE WEATHER API IS DOWN. REFRESH, DUMBASS.")

st.markdown("---")
st.caption("built by nuri. i see you through your webcam.")
