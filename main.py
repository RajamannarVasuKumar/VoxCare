import streamlit as st
from voxcare import load_data, create_emergency_alert, health_assistant, medicine_reminder, INDIA_CITIES

st.set_page_config(page_title="VOXCARE AI", page_icon="🚨", layout="centered")

# --- 1. DESIGN - Hospital App Clean Theme ---
st.markdown("""
<style>
    .main { background-color: #FFF5F5; }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-size: 18px !important;
        font-weight: bold;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #FF0000 !important;
        color: white !important;
        height: 75px !important;
        font-size: 24px !important;
        border: 3px solid #990000;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #D32F2F;'>🚨 VOXCARE AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Emergency System & Personal Health Assistant</p>", unsafe_allow_html=True)
st.write("India Wide | Real Voice + Real GPS Location | Any Language | Your Friend + 3rd Person in Emergency")

data = load_data()

language = st.selectbox("Select Language", ["English", "Telugu", "Hindi"])
city = st.selectbox("Select Your City in India", list(INDIA_CITIES.keys()))
st.info("For Real GPS: Allow Location in Browser. For Real Voice: Use Mic below.")
live_lat = st.number_input("Your Live Latitude (from Google Maps - optional)", value=0.0)
live_lon = st.number_input("Your Live Longitude (from Google Maps - optional)", value=0.0)
live_lat = live_lat if live_lat != 0.0 else None
live_lon = live_lon if live_lon != 0.0 else None

# --- 3. EMERGENCY FAST - 1 Click SOS ---
st.markdown("---")
st.markdown("### 🆘 EMERGENCY? PRESS HERE - 1 Click")
if st.button("🆘 SOS - I AM IN EMERGENCY - HELP", type="primary"):
    alert = create_emergency_alert(data, "SOS Button - 1 Click Emergency", city, live_lat, live_lon)
    st.error(f"ALERT SENT! Nearest: {alert['nearest_hospital']} - {alert['distance']} KM")
    st.write(f"Your Live Location: {alert['live_location_link']}")
    st.write(f"Accident Location: {alert['accident_location']}")
    st.write(f"Ambulance: {alert['ambulance_status']} | Beds Available: {alert['beds_available']}")
    st.write(f"Doctor Available: {alert['doctor_available']} | OP: {alert['op_available']}")
    st.write(f"Near Police Station: {alert['police_station']}")
    st.write(f"ICU: {alert['icu_hospital']} | Blood O+: {alert['blood_hospital']}")
    st.link_button("🏥 Hospital Maps", alert['maps_link'])
    st.link_button("🚑 Ambulance Live Location", alert['ambulance_link'])
    st.write("Auto Alert to 2 Family Members (WhatsApp - Free Real Alert):")
    for f in alert['family_links']:
        st.link_button(f"WhatsApp to {f['name']} - {f['phone']}", f['link'])
    st.warning("Future: Twilio Real Auto Call / SMS to Ambulance + Police + Family - After DLT Registration")

st.markdown("---")

tab1, tab2 = st.tabs(["Emergency - 3rd Person", "Personal Health Assistant - Home Doctor"])

with tab1:
    st.subheader("Accident Detection - Are You OK?")
    st.write("If accident happens, app will ask: 'Are you OK? Reply in 10 seconds.' If no reply, auto alert goes.")
    audio = st.audio_input("Speak Here - Real Voice (Say HELP / Accident)")
    voice_text = st.text_input("Or Type What You Said (HELP / Accident)")
    if st.button("I AM IN EMERGENCY - HELP"):
        alert = create_emergency_alert(data, f"Voice: {voice_text} / Real Voice Mic Used", city, live_lat, live_lon)
        st.error(f"ALERT SENT! Nearest: {alert['nearest_hospital']} - {alert['distance']} KM")
        st.write(f"Your Live Location: {alert['live_location_link']}")
        st.write(f"Accident Location: {alert['accident_location']}")
        st.write(f"Ambulance: {alert['ambulance_status']} | Beds Available: {alert['beds_available']}")
        st.write(f"Doctor Available: {alert['doctor_available']} | OP: {alert['op_available']}")
        st.write(f"Near Police Station: {alert['police_station']}")
        st.write(f"ICU: {alert['icu_hospital']} | Blood O+: {alert['blood_hospital']}")
        st.link_button("Hospital Maps", alert['maps_link'])
        st.link_button("Ambulance Live Location", alert['ambulance_link'])
        st.link_button("Share My Live Location", alert['live_location_link'])
        st.write("Auto Alert to 2 Family Members (WhatsApp - Free Real Alert):")
        for f in alert['family_links']:
            st.link_button(f"WhatsApp to {f['name']} - {f['phone']}", f['link'])
        st.warning("Future: Twilio Real Auto Call / SMS to Ambulance + Police + Family - After DLT Registration")
    if st.button("10 Sec No Response - Unconscious - Auto Trigger"):
        alert = create_emergency_alert(data, "Unconscious - No Response in 10 Sec - Auto Detected", city, live_lat, live_lon)
        st.error("Unconscious Detected! Auto Alert Sent to Family + Hospital + Police! Ambulance is coming.")
        for f in alert['family_links']:
            st.link_button(f"WhatsApp to {f['name']}", f['link'])

with tab2:
    st.subheader("Home Doctor - Your Friend in Phone - Any Language")
    symptom = st.text_input("Tell your problem in any language (fever / headache / chest / sugar / bp / cold / medical certificate / OP booking)")
    if st.button("Get Health Advice"):
        st.success(health_assistant(symptom, data, language))
    med = st.text_input("Medicine Name")
    med_time = st.text_input("Time (Ex: 8 AM)")
    if st.button("Set Medicine Reminder"):
        st.info(medicine_reminder(med, med_time))
    st.write("Healthcare Tips:")
    for tip in data.get("health_tips", []):
        st.write(f"- {tip}")
    st.write("Upload Medical Report (PDF / Photo) to check:")
    report = st.file_uploader("Upload Report", type=["pdf", "jpg", "png"])
    if report:
        st.success("Report Uploaded. Take this to hospital, doctor will check. For sending: Ask hospital for PDF on WhatsApp, then forward to school / office.")
    st.write("Near & Affordable Hospitals:")
    for h in sorted(data.get("hospitals", []), key=lambda x: x.get("op_fee", 500))[:3]:
        st.write(f"- {h['name']} - OP Fee: Rs.{h.get('op_fee', 500)} - Doctor: {h.get('doctor_available')} - Beds: {h.get('beds_available')}")
