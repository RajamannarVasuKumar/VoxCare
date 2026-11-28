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

# --- Clean High-Level Theme & Cards ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #FFF7F7 0%, #FFFFFF 45%, #F8FAFC 100%);
    }
    .hero-box {
        background: #FFFFFF;
        border: 1px solid #FECACA;
        border-left: 6px solid #D32F2F;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(211, 47, 47, 0.08);
        margin-bottom: 14px;
    }
    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 10px;
    }
    .pill-badge {
        background: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FCA5A5;
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 600;
    }
    .chat-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 52px;
        font-size: 16px !important;
        font-weight: 700;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%) !important;
        color: #FFFFFF !important;
        height: 70px !important;
        font-size: 21px !important;
        border: 2px solid #7F1D1D;
        box-shadow: 0 6px 18px rgba(220, 38, 38, 0.28);
    }
</style>
""", unsafe_allow_html=True)

LANG_VOICE_MAP = {
    "English": "en-IN",
    "Telugu": "te-IN",
    "Hindi": "hi-IN",
}


def speak_text(text: str, lang_label: str = "English"):
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
        f"🚨 EMERGENCY DISPATCH READY | Nearest: {alert['nearest_hospital']} ({alert['distance']} KM)"
    )

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("ICU Beds", alert["icu_beds"])
    with m2:
        st.metric("Blood O+", alert["blood_o_plus"])
    with m3:
        st.metric("Ambulance ETA", f"~{alert.get('ambulance_eta_mins', 6)}m")

    st.write(f"📍 **Accident Location:** {alert['accident_location']}")
    st.write(f"🔗 **Live GPS Link:** {alert['live_location_link']}")
    st.write(f"🚓 **Police Station:** {alert['police_station']} (Dial 100 / 112)")
    st.write(f"🚑 **Ambulance:** {alert['ambulance_status']} (Dial 108)")
    st.write(
        f"🏥 **Hospital Status:** Beds: {alert['beds_available']} | "
        f"Doctor: {alert['doctor_available']} | OP: {alert['op_available']}"
    )

    st.info(
        f"🪪 **Medical ID:** Blood Group: {med_id.get('blood_group', 'O+')} | "
        f"Allergies: {med_id.get('allergies', 'Check before medication')} | "
        f"Notes: {med_id.get('conditions', 'None major recorded')}"
    )

    if show_ambulance_tracker:
        st.markdown("#### 🚑 Ambulance Live Tracker (Conscious Victim View)")
        eta = alert.get("ambulance_eta_mins", 6)
        st.success(f"Status: En Route | Estimated Arrival: ~{eta} minutes | Flow: Alert -> Dispatched -> Approaching")
        st.progress(68)

    st.link_button("📍 Open Live GPS Location", alert["live_location_link"])
    st.link_button("🏥 Nearest Hospital Maps", alert["maps_link"])
    st.link_button("🚑 Ambulance Route Maps", alert["ambulance_link"])
    st.link_button("🚓 Police Station Maps", alert["police_link"])

    st.markdown("**📲 Instant Family Alert (WhatsApp Live Location):**")
    for f in alert.get("family_links", []):
        st.link_button(f"Alert {f['name']} ({f['phone']})", f["link"])


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_alert" not in st.session_state:
    st.session_state.active_alert = None
if "crash_check_pending" not in st.session_state:
    st.session_state.crash_check_pending = False

data = load_data()
med_id = data.get("medical_id", {})

st.markdown("""
<div class="hero-box">
    <h1 style="text-align: center; color: #B91C1C; margin: 0;">🚨 VOXCARE AI</h1>
    <p style="text-align: center; font-size: 16px; color: #334155; margin: 6px 0 0 0;">
        India-Wide Voice Health Friend &amp; 3rd-Person Accident Guardian
    </p>
    <div class="badge-row">
        <span class="pill-badge">🇮🇳 India-Wide Any City</span>
        <span class="pill-badge">🎙️ Voice + Screen Text</span>
        <span class="pill-badge">📍 Live GPS + Maps</span>
        <span class="pill-badge">🚑 Primary Helpline: 108 / 112</span>
    </div>
</div>
""", unsafe_allow_html=True)

language = st.selectbox("Select Language", ["English", "Telugu", "Hindi"])

city_options = list(INDIA_CITIES.keys()) + ["Other Indian City (Type Any City / Town)"]
selected_city_option = st.selectbox("Select Your City in India", city_options)

if selected_city_option == "Other Indian City (Type Any City / Town)":
    custom_city = st.text_input("Enter Your City & State in India", value="Visakhapatnam, AP")
    city = (custom_city or "").strip() or "India"
else:
    city = selected_city_option

c1, c2 = st.columns(2)
with c1:
    live_lat_val = st.number_input("Live Latitude (optional)", value=0.0, format="%.4f")
with c2:
    live_lon_val = st.number_input("Live Longitude (optional)", value=0.0, format="%.4f")

live_lat = live_lat_val if live_lat_val != 0.0 else None
live_lon = live_lon_val if live_lon_val != 0.0 else None

st.markdown("---")
st.markdown("### 🆘 EMERGENCY? PRESS HERE — 1 CLICK")
if st.button("🆘 SOS - I AM IN EMERGENCY - HELP", type="primary"):
    alert = create_emergency_alert(data, "SOS Button - 1 Click Emergency", city, live_lat, live_lon)
    st.session_state.active_alert = alert
    spoken = (
        f"Emergency alert activated in {city}! Nearest hospital is {alert['nearest_hospital']}. "
        f"Ambulance estimated arrival is {alert['ambulance_eta_mins']} minutes."
    )
    speak_text(spoken, language)

if st.session_state.active_alert:
    render_alert_details(st.session_state.active_alert, med_id, show_ambulance_tracker=True)

st.markdown("---")

tab1, tab2 = st.tabs(["🚨 Crash & 3rd-Person Emergency", "🩺 Health Friend (Voice + Text)"])

with tab1:
    st.subheader("Car Crash / Jerk Detection & 10s Check")
    st.write(
        "If a sudden impact happens anywhere in India, VoxCare asks 'Are you okay?' "
        "With no response in 10 seconds, emergency dispatch details prepare for Family, Police, Ambulance, and Hospital."
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
            f"No response in 10 seconds. Emergency mode activated in {city} for "
            f"{alert['nearest_hospital']}."
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
            f"Emergency details ready for {city}. Nearest hospital is {alert['nearest_hospital']}, "
            f"{alert['distance']} kilometers away."
        )
        speak_text(spoken, language)
        st.rerun()

with tab2:
    st.subheader("Health Friend - Talk & Read Together")
    st.write("Ask any health topic—get both spoken voice-over and clear text on screen.")

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
        speak_text(reply, language)

    for item in reversed(st.session_state.chat_history[-5:]):
        st.markdown(
            f"""
            <div class="chat-card">
                <div style="font-size: 13px; color: #64748B;"><b>You:</b> {item['you']}</div>
                <div style="font-size: 15px; color: #0F172A; margin-top: 6px;"><b>VoxCare Friend:</b> {item['friend']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
