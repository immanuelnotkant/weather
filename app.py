import streamlit as st
import requests
import base64
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="666", layout="centered")

# --- DATA FETCHING ---
city_data = streamlit_js_eval(js_expressions='fetch("https://ipapi.co/json/").then(response => response.json())', key='LOCATION')

# Function to encode the image
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
            background-size: 100% 100%; /* FORCES IMAGE TO FIT WINDOW EXACTLY */
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.5); /* Slightly clearer so the face is visible */
            z-index: -1;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except:
        st.markdown("<style>.stApp { background-color: black; }</style>", unsafe_allow_html=True)

# Set the background image
set_background('images.jpeg')

# --- THE MASKED BALL AUDIO ---
# This uses a direct link to the haunting choral chant
st.markdown(
    """
    <audio autoplay loop>
      <source src="https://archive.org/download/eyes-wide-shut-masked-ball/Eyes%20Wide%20Shut%20-%20Masked%20Ball.mp3" type="audio/mpeg">
    </audio>
    <style>
    audio { display:none; }
    </style>
    """,
    unsafe_allow_html=True
)

def get_weather_theme(condition):
    cond = condition.lower()
    if "thunder" in cond or "storm" in cond:
        return "animation: flash 0.1s infinite;", "THE CEREMONY HAS BEGUN."
    elif "rain" in cond:
        return "animation: bleed 0.5s infinite;", "THE SKY WEEPS FOR YOUR SINS."
    elif "clear" in cond or "sun" in cond:
        return "animation: pulse 2s infinite;", "THE LIGHT REVEALS EVERYTHING."
    return "opacity: 0.9;", "FIDELIO."

# --- APP LOGIC ---
if not city_data:
    st.markdown("<h1 style='color:red; text-align:center; font-family:Courier;'>ENTERING THE MANSION...</h1>", unsafe_allow_html=True)
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
    font-size: clamp(60px, 12vw, 120px);
    text-align: center;
    text-shadow: 0 0 30px #ff0000;
    margin-top: 10%;
    font-weight: bold;
    {anim}
}}
</style>
<div class="main-text">{city}</div>
<h2 style='text-align:center; text-shadow: 2px 2px #000; color: white;'>{temp}°C — {cond}</h2>
"""
        st.markdown(html_block, unsafe_allow_html=True)
        st.error(threat)
    else:
        st.error("THE PASSWORD IS INCORRECT.")

st.markdown("---")
st.caption("built by nuri. i see you through your webcam.")

st.markdown("---")
st.caption("built by nuri. i see you through your webcam.")
