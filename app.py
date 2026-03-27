import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="666", page_icon="👹", layout="centered")

# Schizo/Hell Styling
st.markdown("""
    <style>
    body, [data-testid="stAppViewContainer"] {
        background-color: #000000;
        color: #ff0000;
        font-family: 'Courier New', Courier, monospace;
    }
    .glitch {
        color: #ff0000;
        font-size: 80px;
        text-align: center;
        text-shadow: 5px 5px #550000;
        animation: freak 0.1s infinite;
    }
    @keyframes freak {
        0% { skew(2deg); opacity: 0.8; }
        50% { skew(-2deg); opacity: 1; }
        100% { skew(3deg); opacity: 0.5; }
    }
    .stMetric {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid #ff0000;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# THE JAVASCRIPT HACK - This grabs the visitor's IP, not the server's.
# We use a public API called 'ipify' to get the user's real IP first.
components.html(
    """
    <script>
    fetch('https://ipapi.co/json/')
      .then(response => response.json())
      .then(data => {
        window.parent.postMessage({
          type: 'streamlit:set_widget_value',
          data: data.city,
          key: 'user_city'
        }, '*');
      });
    </script>
    """,
    height=0,
)

# Pull the city from the Javascript injection
city_name = st.session_state.get('user_city', 'SEARCHING...')

def get_weather(city):
    API_KEY = "f37ab49ad8ebaac85adbe8bd2d9c9b91"
    
    if city == "SEARCHING...":
        st.markdown('<p class="glitch">WE ARE FINDING YOU</p>', unsafe_allow_html=True)
        return

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") == 200:
            temp = round(data['main']['temp'])
            st.markdown(f'<p class="glitch">{city.upper()}</p>', unsafe_allow_html=True)
            
            st.write(f"### {temp}°C | {data['weather'][0]['description'].upper()}")
            st.error("THEY ARE INSIDE THE WALLS. DON'T LOOK LEFT.")
            
        elif data.get("cod") == 401:
            st.markdown(f'<p class="glitch">{city.upper()}</p>', unsafe_allow_html=True)
            st.error("I KNOW YOUR CITY BUT THE API IS LOADING YOU FUCKING DUMBASS. REFRESH.")
    except:
        st.write("EYES EYES EYES EYES EYES")

get_weather(city_name)

# Creepy footer
st.markdown("---")
st.caption("built by nuri. i see you through the webcam.")
