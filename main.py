import time
import streamlit as st
import streamlit.components.v1 as components
from voxcare import (
    load_data,
    check_voice,
    create_emergency_alert,
    health_assistant,
    medicine_reminder,
    INDIA_CITIES,
)

st.set_page_config(page_title="VOXCARE AI", page_icon="🚨", layout="centered")

# --- 1. DESIGN - Clean Hospital & Emergency Theme ---
st.markdown("""
<style>
    .main { background-color: #FFF5F5; }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 54px;
        font-size: 17px !important;
        font-weight: bold;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #D32F2F !important;
        color: white !important;
        height: 72px !important;
        font-size: 22px !important;
        border: 2px solid #8E0000;
    }
</style>
""", unsafe_allow_html=True)

LANG_VOICE_MAP = {
    "English": "en-IN",
    "Telugu": "te-IN",
    "Hindi": "hi-IN",
}


def speak_text(text: str, lang_label: str = "English"):
    """Zero-cost browser TTS so the app speaks aloud while text stays visible on screen."""
    if not text:
        return
    clean_text = (
        str(text)
        .replace('"', "")
        .replace("'", "")
        .replace("\n", ". ")
        .replace("*", "")
        .replace("#", "")
    )
    voice_lang = LANG_VOICE_MAP.get(lang_label, "en-IN")
    js_code = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.lang = "{voice_lang}";
                msg.rate = 0.98;
                msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
            }}
        }})();
    </script>
    """
    components.html(js_code, height=0)


def render_alert_details(alert: dict, med_id: dict, show_ambulance_tracker: bool = True):
    st.error(
        f"EMERGENCY ALERT ACTIVE | Nearest Hospital: {alert['nearest_hospital']} ({alert['distance']} KM)"
    )
    st.markdown("**Live GPS Location Dispatched To: Family, Police Station, Ambulance (108), Nearest Hospital**")
    st.write(f"- **Accident Live GPS:** {alert['live_location_link']} ({alert['accident_location']})")
    st.write(f"- **Police Station:** {alert['police_station']} (Emergency Dial: 100 / 112)")
    st.write(f"- **Ambulance Status:** {alert['ambulance_status']} (Emergency Dial: 108)")
    st.write(
        f"- **Hospital Readiness:** ICU Beds: {alert['icu_beds']} | "
        f"Blood Bank (O+): {alert['blood_o_plus']} units | "
        f"General Beds: {alert['beds_available']} | OP: {alert['op_available']}"
    )
    st.write(f"- **On-Duty Doctor:** {alert['doctor_available']}")

    st.markdown("**Medical ID (Golden Hour Info):**")
    st.info(
        f"Blood Group: {med_id.get('blood_group', 'O+')} | "
        f"Allergies: {med_id.get('allergies', 'None')} | "
        f"Conditions: {med_id.get('conditions', 'None')}"
    )

    if show_ambulance_tracker:
        st.markdown("### 🚑 Ambulance Live Location Tracker (For Conscious Victim)")
        eta = alert.get("ambulance_eta_mins", 6)
        st.success(
            f"Ambulance Status: Dispatched & En Route | Estimated Arrival: ~{eta} mins | "
            f"Route Stage: Alert Sent -> Dispatched -> Approaching ({eta}m)"
        )
        st.progress(65)

    st.link_button("📍 Open Accident Live GPS", alert["live_location_link"])
    st.link_button("🏥 Nearest Hospital on Maps", alert["maps_link"])
    st.link_button("🚑 Ambulance Route on Maps", alert["ambulance_link"])
    st.link_button("🚓 Nearby Police Station on Maps", alert["police_link"])

    st.markdown("**Instant Family Alert (WhatsApp Live Location Link):**")
    for f in alert.get("family_links", []):
        st.link_button(f"📲 Alert {f['name']} ({f['phone']})", f["link"])


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_alert" not in st.session_state:
    st.session_state.active_alert = None
if "crash_check_pending" not in st.session_state:
    st.session_state.crash_check_pending = False

data = load_data()
med_id = data.get("medical_id", {})

st.markdown("<h1 style='text-align: center; color: #D32F2F;'>🚨 VOXCARE AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 18px;'>India-Wide Voice Health Friend & 3rd-Person Accident Guardian</p>",
    unsafe_allow_html=True,
)
st.write("India Wide (Any City / State) | Voice + Screen Text | Live GPS Sharing | Hospital ICU & Blood Readiness")

language = st.selectbox("Select Language", ["English", "Telugu", "Hindi"])

city_options = list(INDIA_CITIES.keys()) + ["Other Indian City (Type Any City / Town)"]
selected_city_option = st.selectbox("Select Your City in India", city_options)

if selected_city_option == "Other Indian City (Type Any City / Town)":
    custom_city = st.text_input("Enter Your City & State in India (e.g., Visakhapatnam, AP or Kochi, Kerala)", value="India")
    city = (custom_city or "").strip() or "India"
else:
    city = selected_city_option

col1, col2 = st.columns(2)
with col1:
    live_lat_val = st.number_input("Your Live Latitude (optional)", value=0.0, format="%.4f")
with col2:
    live_lon_val = st.number_input("Your Live Longitude (optional)", value=0.0, format="%.4f")

live_lat = live_lat_val if live_lat_val != 0.0 else None
live_lon = live_lon_val if live_lon_val != 0.0 else None

# --- 1-CLICK SOS ---
st.markdown("---")
st.markdown("### 🆘 EMERGENCY? PRESS HERE - 1 CLICK")
if st.button("🆘 SOS - I AM IN EMERGENCY - HELP", type="primary"):
    alert = create_emergency_alert(data, "SOS Button - 1 Click Emergency", city, live_lat, live_lon)
    st.session_state.active_alert = alert
    spoken = (
        f"Emergency alert activated in {city}! Live location is ready for family, police, ambulance, and "
        f"{alert['nearest_hospital']}. Ambulance estimated arrival is {alert['ambulance_eta_mins']} minutes."
    )
    speak_text(spoken, language)

if st.session_state.active_alert:
    render_alert_details(st.session_state.active_alert, med_id, show_ambulance_tracker=True)

st.markdown("---")

tab1, tab2 = st.tabs(["🚨 Crash & 3rd-Person Emergency", "🩺 Health Friend (Voice + Text)"])

with tab1:
    st.subheader("Car Crash / Jerk Detection & Consciousness Check")
    st.write(
        "If a sudden crash/jerk happens anywhere in India, VoxCare asks: 'Are you okay?' "
        "If unconscious or no reply in 10 seconds, auto emergency alerts prepare for Family, Police, Ambulance, and Hospital."
    )

    if st.button("💥 Simulate Car Jerk / Crash (10s 'Are You Okay?' Check)"):
        st.session_state.crash_check_pending = True
        speak_text("Sudden impact detected! Are you okay? Respond within 10 seconds.", language)

    if st.session_state.crash_check_pending:
        st.warning("Are you okay? Checking response over 10 seconds...")
        timer_box = st.empty()
        for sec in range(10, 0, -1):
            timer_box.info(f"⏳ Consciousness Check: {sec} seconds remaining...")
            time.sleep(0.35)
        st.session_state.crash_check_pending = False
        alert = create_emergency_alert(
            data,
            "Car Crash / Jerk - Unconscious or No Response in 10s",
            city,
            live_lat,
            live_lon,
        )
        st.session_state.active_alert = alert
        unconscious_msg = (
            f"No response in 10 seconds. Unconscious emergency mode triggered in {city}! "
            f"Alerting family, police, ambulance, and {alert['nearest_hospital']} with live location."
        )
        speak_text(unconscious_msg, language)
        st.rerun()

    audio = st.audio_input("Speak Here - Voice Emergency (Say HELP / Accident)")
    if audio is not None:
        st.success("Voice recorded! Tap 'Trigger Voice / Conscious Emergency' below.")

    voice_text = st.text_input("Or Type Spoken Emergency Message (e.g., HELP / Accident)")
    if st.button("🚨 Trigger Voice / Conscious Emergency"):
        is_kw = check_voice(voice_text)
        reason = f"Voice Alert ({voice_text})" if voice_text else "Voice Mic Emergency Triggered"
        if is_kw:
            reason = f"Urgent Keyword Detected ({voice_text})"
        alert = create_emergency_alert(data, reason, city, live_lat, live_lon)
        st.session_state.active_alert = alert
        spoken = (
            f"Help is being coordinated in {city}. Nearest hospital is {alert['nearest_hospital']}, "
            f"{alert['distance']} kilometers away. Ambulance ETA is {alert['ambulance_eta_mins']} minutes."
        )
        speak_text(spoken, language)
        st.rerun()

with tab2:
    st.subheader("Health Friend - Talk & Read Together")
    st.write("Ask any health topic—like a caring friend, you get both spoken voice and clear text on screen.")

    health_audio = st.audio_input("Speak Your Health Question (Voice Input)")
    if health_audio is not None:
        st.info("Voice recorded! Enter or review your health question below and tap Ask Health Friend.")

    symptom = st.text_input(
        "Ask any health question (fever, headache, sleep, diet, sugar, BP, cold, OP booking, medical certificate)"
    )

    if st.button("💬 Ask Health Friend (Text + Voice)"):
        question_text = (symptom or "").strip()
        if not question_text and health_audio is not None:
            question_text = "Voice health question recorded"
        reply = health_assistant(question_text, data, language)
        st.session_state.chat_history.append({
            "you": question_text if question_text else "(Empty prompt)",
            "friend": reply,
        })
        st.success(reply)
        speak_text(reply, language)

    if st.session_state.chat_history:
        st.markdown("**Recent Conversation:**")
        for item in reversed(st.session_state.chat_history[-5:]):
            st.write(f"**You:** {item['you']}")
            st.write(f"**VoxCare Friend:** {item['friend']}")
            st.markdown("---")

    med = st.text_input("Medicine Name for Reminder")
    med_time = st.text_input("Reminder Time (e.g., 8:00 AM)")
    if st.button("⏰ Set Medicine Reminder"):
        reminder_msg = medicine_reminder(med, med_time)
        st.info(reminder_msg)
        speak_text(reminder_msg, language)

    st.markdown("**Daily Health Tips:**")
    for tip in data.get("health_tips", []):
        st.write(f"- {tip}")

    st.markdown("**Upload Medical Report (PDF / Photo):**")
    report = st.file_uploader("Upload Report", type=["pdf", "jpg", "png"])
    if report:
        msg_rep = "Report uploaded. Carry it with OPD slip to the doctor, or request a signed PDF on WhatsApp/Email to share."
        st.success(msg_rep)
        speak_text(msg_rep, language)

    st.markdown("**Nearby Hospitals (OP, Beds, ICU & O+ Blood Status):**")
    for h in data.get("hospitals", []):
        o_plus = h.get("blood_bank", {}).get("O+", 0)
        st.write(
            f"- **{h['name']}** ({h.get('city', '')}) — OP Fee: Rs.{h.get('op_fee', 200)} | "
            f"ICU: {h.get('icu_beds', 0)} | O+ Blood: {o_plus} | Beds: {h.get('beds_available', 0)}"
)
