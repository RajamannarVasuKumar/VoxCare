import json
import os
from datetime import datetime
import urllib.parse

try:
    from google import genai
except ImportError:
    genai = None

INDIA_CITIES = {
    "Guntur, AP": {"lat": 16.3067, "lon": 80.4365},
    "Hyderabad, Telangana": {"lat": 17.3850, "lon": 78.4867},
    "Delhi": {"lat": 28.7041, "lon": 77.1025},
    "Mumbai, Maharashtra": {"lat": 19.0760, "lon": 72.8777},
    "Bengaluru, Karnataka": {"lat": 12.9716, "lon": 77.5946},
    "Chennai, Tamil Nadu": {"lat": 13.0827, "lon": 80.2707},
    "Vijayawada, AP": {"lat": 16.5062, "lon": 80.6480},
    "Visakhapatnam, AP": {"lat": 17.6868, "lon": 83.2185},
    "Kolkata, West Bengal": {"lat": 22.5726, "lon": 88.3639},
    "Pune, Maharashtra": {"lat": 18.5204, "lon": 73.8567},
    "Ahmedabad, Gujarat": {"lat": 23.0225, "lon": 72.5714},
    "Jaipur, Rajasthan": {"lat": 26.9124, "lon": 75.7873},
    "Kochi, Kerala": {"lat": 9.9312, "lon": 76.2673},
    "Bhubaneswar, Odisha": {"lat": 20.2961, "lon": 85.8245},
    "Lucknow, Uttar Pradesh": {"lat": 26.8467, "lon": 80.9462},
    "Guwahati, Assam": {"lat": 26.1445, "lon": 91.7362},
}

EMERGENCY_KEYWORDS = [
    "help", "ambulance", "help me", "padipoyanu", "kapadandi",
    "emergency", "doctor", "bachao", "accident", "madad"
]


def load_data():
    try:
        with open("hospitals.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "medical_id": {
                "blood_group": "O+",
                "allergies": "None known",
                "conditions": "None known",
                "emergency_note": "Check conscious response first. Share live GPS immediately.",
            },
            "hospitals": [],
            "family_contacts": [],
            "health_tips": [],
            "medicines": {},
        }


def check_voice(text):
    if not text:
        return False
    return any(w in text.lower() for w in EMERGENCY_KEYWORDS)


def _resolve_coordinates(city, live_lat=None, live_lon=None):
    if live_lat is not None and live_lon is not None:
        return float(live_lat), float(live_lon)

    if city in INDIA_CITIES:
        return INDIA_CITIES[city]["lat"], INDIA_CITIES[city]["lon"]

    city_clean = (city or "").strip().lower()
    for name, coords in INDIA_CITIES.items():
        if city_clean and (city_clean in name.lower() or name.lower() in city_clean):
            return coords["lat"], coords["lon"]

    # Default center of India fallback if custom city is not in preset dictionary
    return 20.5937, 78.9629


def create_emergency_alert(data, reason, city="Guntur, AP", live_lat=None, live_lon=None):
    city_label = (city or "India").strip() or "India"
    lat, lon = _resolve_coordinates(city_label, live_lat, live_lon)

    city_lower = city_label.lower()
    hospitals = [
        h for h in data.get("hospitals", [])
        if city_lower in str(h.get("city", "")).lower() or str(h.get("city", "")).lower() in city_lower
    ]
    if not hospitals:
        hospitals = data.get("hospitals", [])

    hospitals = sorted(hospitals, key=lambda x: x.get("distance_km", 999))
    nearest = hospitals[0] if hospitals else None

    maps_link = f"https://www.google.com/maps/search/hospital+near+{lat},{lon}"
    ambulance_link = f"https://www.google.com/maps/search/ambulance+near+{lat},{lon}"
    police_link = f"https://www.google.com/maps/search/police+station+near+{lat},{lon}"
    live_link = f"https://www.google.com/maps?q={lat},{lon}"

    nearest_name = (
        nearest["name"]
        if nearest and nearest.get("name")
        else f"Nearest Hospital in {city_label}"
    )
    o_plus_units = nearest.get("blood_bank", {}).get("O+", 6) if nearest else 6
    icu_count = nearest.get("icu_beds", 4) if nearest else 4

    msg = (
        f"VOXCARE AI EMERGENCY: {reason} in {city_label}, India. "
        f"Live Location: {live_link}. "
        f"Nearest Hospital: {nearest_name} (ICU: {icu_count}, O+ Blood: {o_plus_units}). "
        f"Ambulance: 108 | Police: 100 / 112. "
        f"Hospital Map: {maps_link}"
    )

    wa_links = []
    for person in data.get("family_contacts", []):
        phone_clean = (
            str(person.get("phone", ""))
            .replace("+", "")
            .replace("-", "")
            .replace(" ", "")
        )
        wa_links.append({
            "name": person.get("name", "Family Contact"),
            "phone": person.get("phone", ""),
            "link": f"https://wa.me/{phone_clean}?text={urllib.parse.quote(msg)}",
        })

    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reason": reason,
        "city": city_label,
        "accident_location": f"{city_label}, India ({lat:.4f}, {lon:.4f})",
        "live_location_link": live_link,
        "nearest_hospital": nearest_name,
        "distance": nearest["distance_km"] if nearest and "distance_km" in nearest else 2.0,
        "icu_hospital": nearest_name if icu_count > 0 else "Check Nearby ICU",
        "icu_beds": icu_count,
        "blood_hospital": nearest_name if o_plus_units > 0 else "Check Nearby Blood Bank",
        "blood_o_plus": o_plus_units,
        "police_station": (
            nearest.get("police_station", f"Nearest Police Station - {city_label} (Dial 100 / 112)")
            if nearest
            else f"Nearest Police Station - {city_label} (Dial 100 / 112)"
        ),
        "police_link": police_link,
        "ambulance_status": (
            nearest.get("ambulance", "108 Ambulance Ready - Dispatched")
            if nearest
            else "108 Ambulance Ready - Dispatched"
        ),
        "ambulance_eta_mins": (
            nearest.get("ambulance_eta_mins", 7)
            if nearest
            else 7
        ),
        "doctor_available": (
            nearest.get("doctor_available", "24x7 Emergency & Duty Doctor Available")
            if nearest
            else "24x7 Emergency & Duty Doctor Available"
        ),
        "op_available": (
            nearest.get("op_available", "OP & Casualty Available")
            if nearest
            else "OP & Casualty Available"
        ),
        "beds_available": nearest.get("beds_available", 12) if nearest else 12,
        "maps_link": maps_link,
        "ambulance_link": ambulance_link,
        "family_links": wa_links,
        "family": data.get("family_contacts", []),
        "dispatch_summary": msg,
    }


def _rule_based_health_reply(symptom, data, language="English"):
    s = (symptom or "").strip().lower()
    if not s:
        return "Hey friend, I am right here with you. Tell me your health question or symptom and I will help."

    meds = data.get("medicines", {})
    prefix = {
        "Telugu": "Nee problem ki: ",
        "Hindi": "Aapki samasya ke liye: ",
        "English": "",
    }.get(language, "")

    def med_or_default(key, fallback):
        val = meds.get(key)
        return val if val else fallback

    if "fever" in s or "jwaram" in s or "bukhar" in s:
        med = med_or_default("fever", "ask a doctor or pharmacist")
        return f"{prefix}For fever, drink plenty of water and take rest. Common option: {med}. If it does not reduce in 2 days, visit a hospital."
    if "headache" in s or "thalaka" in s or "sir dard" in s:
        med = med_or_default("headache", "rest in a quiet room and stay hydrated")
        return f"{prefix}For headache, rest and drink water. Helpful step: {med}."
    if "chest" in s or "gundelo" in s or "seene" in s:
        return "Chest pain can be a serious EMERGENCY. Please press HELP immediately or call 108."
    if "sugar" in s or "diabetes" in s or "madhumeham" in s:
        med = med_or_default("sugar", "follow your doctor prescribed diet and medication")
        return f"{prefix}For blood sugar care, try 30 minutes of daily walking and {med}."
    if "bp" in s or "pressure" in s:
        med = med_or_default("bp", "reduce salt and check BP regularly")
        return f"{prefix}For BP care, reduce excess salt and {med}."
    if "cold" in s or "jalubu" in s or "sardi" in s:
        med = med_or_default("cold", "take warm water and rest")
        return f"{prefix}For cold, drink warm fluids, rest, and {med}."
    if "certificate" in s or "report" in s:
        return (
            "For a medical certificate or report, take your OPD slip, ID proof, and old reports to the hospital doctor. "
            "Get doctor signature and seal, or ask for the PDF on WhatsApp or email to share."
        )
    if "op" in s or "appointment" in s or "book" in s:
        return (
            "To book OP from home, check the hospital link in the emergency section, call the hospital desk, "
            "or open the hospital on Google Maps to book an appointment."
        )
    return f"{prefix}Take rest, drink water, and eat light healthy food. If symptoms continue, consult a doctor. For urgent help, press HELP."


def health_assistant(symptom, data, language="English"):
    cleaned = (symptom or "").strip()
    if not cleaned:
        return "Hey friend, I am right here with you. Tell me your health question or symptom so I can help."

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if api_key and genai is not None:
        try:
            client = genai.Client(api_key=api_key)
            prompt = (
                f"You are VoxCare AI, a caring, supportive friend and health guide helping users across India. "
                f"Selected language preference: {language}. "
                f"Reply warmly and clearly in natural English (or friendly English-Telugu if Telugu is selected). "
                f"Keep the answer around 3 to 4 short, easy-to-hear sentences so text-to-speech sounds smooth. "
                f"Do not use markdown symbols like *, #, or bullet lists. "
                f"Encourage consulting a doctor for serious or ongoing issues. "
                f"User asks: {cleaned}"
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            if response and response.text:
                return response.text.strip()
        except Exception:
            pass

    return _rule_based_health_reply(cleaned, data, language)


def medicine_reminder(medicine, time_str):
    med_name = (medicine or "").strip() or "your medicine"
    timing = (time_str or "").strip() or "scheduled time"
    return f"Reminder Set: Take {med_name} at {timing}."
