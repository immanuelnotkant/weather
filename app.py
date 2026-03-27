import streamlit as st
import requests
import base64
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="666", layout="centered")

# --- DATA FETCHING ---
city_data = streamlit_js_eval(js_expressions='fetch("https://ipapi.co/json/").then(response => response.json())', key='LOCATION')

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
            background-size: 100% 100%; /* FORCES IMAGE TO FIT WINDOW */
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: -1;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except:
        st.markdown("<style>.stApp {{ background-color: black; }}</style>", unsafe_allow_html=True)

# Ensure the file in your GitHub repo is named images.jpeg
set_background('images.jpeg')

# --- AUTHENTICATION GATE ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("<h1 style='color:red; text-align:center; font-family:Courier;'>UNDER THE MASK...</h1>", unsafe_allow_html=True)
    pw = st.text_input("ENTER THE PASSWORD", type="password")
    if pw.lower() == "fidelio":
        st.session_state['auth'] = True
        st.rerun()
    st.stop()

# --- THE EXTENDED MASKED BALL MUSIC ---
# This loads the specific YouTube video you provided as a hidden, autoplaying loop
st.markdown(
    """
    <iframe src="https://www.youtube.com/embed/fHRLoVmPeLU?autoplay=1&loop=1&playlist=fHRLoVmPeLU" 
    width="0" height="0" frameborder="0" allow="autoplay"></iframe>
    """, 
    unsafe_allow_html=True
)

# --- WEATHER DISPLAY ---
if city_data:
    city = city_data.get('city', 'NOWHERE').upper()
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") == 200:
        temp = round(data['main']['temp'])
        cond = data['weather'][0]['description'].upper()
        
        st.markdown(f"<h1 style='font-size:80px; text-align:center; color:red; text-shadow: 0 0 20px #ff0000; font-family:Courier;'>{city}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:white; font-family:Courier;'>{temp}°C — {cond}</h2>", unsafe_allow_html=True)
        st.error("FIDELIO.")

st.markdown("---")
st.caption("built by nuri. i see you through your webcam.")
