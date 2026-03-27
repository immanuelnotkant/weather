import streamlit as st
import requests
import base64
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Weather Station", layout="centered")

# --- DATA FETCHING ---
city_data = streamlit_js_eval(js_expressions='fetch("https://ipapi.co/json/").then(response => response.json())', key='LOCATION')

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- STATE MANAGEMENT ---
if 'activated' not in st.session_state:
    st.session_state['activated'] = False

# --- UI LOGIC ---
if not st.session_state['activated']:
    # THE "CALM" STARTING SCREEN
    st.markdown("""
        <style>
        .stApp { background-color: #000000; }
        .enter-btn {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
        }
        button {
            background-color: transparent !important;
            color: #333 !important;
            border: 1px solid #111 !important;
            font-family: 'Courier New', monospace !important;
            padding: 10px 20px !important;
        }
        button:hover {
            color: #600 !important;
            border-color: #600 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.write("") # Padding
    if st.button("CLICK TO SEE THE WEATHER"):
        st.session_state['activated'] = True
        st.rerun()

else:
    # THE "SCARY" ACTIVATED SCREEN
    try:
        bin_str = get_base64('images.jpeg')
        st.markdown(f'''
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: 100% 100%;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: #ff0000 !important;
                font-family: 'Courier New', monospace;
            }}
            .stApp::before {{
                content: "";
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background-color: rgba(0, 0, 0, 0.4);
                z-index: -1;
            }}
            .main-text {{
                font-size: 100px;
                text-align: center;
                text-shadow: 0 0 30px #ff0000;
                margin-top: 50px;
                font-weight: bold;
                animation: shake 0.2s infinite;
            }}
            @keyframes shake {{
                0% {{ transform: translate(1px, 1px); }}
                50% {{ transform: translate(-1px, -1px); }}
                100% {{ transform: translate(1px, -1px); }}
            }}
            </style>
        ''', unsafe_allow_html=True)
    except:
        st.error("IMAGE FILE MISSING")

    # HIDDEN MUSIC PLAYER (Extended Mix)
    st.markdown(
        """
        <iframe src="https://www.youtube.com/embed/fHRLoVmPeLU?autoplay=1&loop=1&playlist=fHRLoVmPeLU" 
        width="0" height="0" frameborder="0" allow="autoplay"></iframe>
        """, 
        unsafe_allow_html=True
    )

    if city_data:
        city = city_data.get('city', 'NOWHERE').upper()
        API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91" 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") == 200:
            temp = round(data['main']['temp'])
            cond = data['weather'][0]['description'].upper()
            
            st.markdown(f'<div class="main-text">{city}</div>', unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center; color:white;'>{temp}°C — {cond}</h2>", unsafe_allow_html=True)
            st.error("I AM BEHIND THE CURTAIN.")

    st.markdown("---")
    st.caption("built by nuri. i see you through your webcam.")
