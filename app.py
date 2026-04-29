import streamlit as st
import requests
import base64
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Weather Station", layout="centered")


city_data = streamlit_js_eval(js_expressions='fetch("https://ipapi.co/json/").then(response => response.json())', key='LOCATION')

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None


if 'activated' not in st.session_state:
    st.session_state['activated'] = False


if not st.session_state['activated']:
    st.markdown("""
        <style>
        .stApp { background-color: #000000; }
        .stButton button {
            background-color: #8b0000 !important; /* Solid Dark Red */
            color: white !important;
            border: 2px solid #ff0000 !important; /* Bright Red Glow Border */
            font-family: 'Courier New', monospace !important;
            font-weight: bold;
            margin-top: 300px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            padding: 15px 35px;
            transition: 0.3s;
        }
        .stButton button:hover {
            background-color: #ff0000 !important;
            color: black !important;
            box-shadow: 0 0 25px #ff0000;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("CLICK TO SEE THE WEATHER"):
        st.session_state['activated'] = True
        st.rerun()

else:
 
    bin_str = get_base64('images.jpeg')
    if bin_str:
        st.markdown(f'''
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: #ff0000 !important;
                font-family: 'Courier New', monospace;
            }}
            .main-text {{
                font-size: clamp(50px, 10vw, 100px);
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
    else:
        st.error("THE FACE IS MISSING.")


    st.markdown(
        """
        <iframe src="https://www.youtube.com/embed/fHRLoVmPeLU?autoplay=1&start=28&controls=0" 
        width="1" height="1" style="position:absolute; top:0; left:0; opacity:0.01; pointer-events:none;" 
        frameborder="0" allow="autoplay; encrypted-media"></iframe>
        """, 
        unsafe_allow_html=True
    )

    if city_data:
        city = city_data.get('city', 'NOWHERE').upper()
        API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91" 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url).json()
            if response.get("cod") == 200:
                temp = round(response['main']['temp'])
                cond = response['weather'][0]['description'].upper()
                
                st.markdown(f'<div class="main-text">{city}</div>', unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align:center; color:white; text-shadow: 2px 2px 5px black;'>{temp}°C — {cond}</h2>", unsafe_allow_html=True)
                st.error("I AM BEHIND THE CURTAIN.")
        except:
            st.warning("COULD NOT FETCH WEATHER DATA.")

    st.markdown("---")
    st.caption("built by nuri. i see you through your webcam.")
