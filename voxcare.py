import json
from datetime import datetime
import urllib.parse

INDIA_CITIES = {
    "Guntur, AP": {"lat": 16.3067, "lon": 80.4365},
    "Hyderabad, Telangana": {"lat": 17.3850, "lon": 78.4867},
    "Delhi": {"lat": 28.7041, "lon": 77.1025},
    "Mumbai, Maharashtra": {"lat": 19.0760, "lon": 72.8777},
    "Bengaluru, Karnataka": {"lat": 12.9716, "lon": 77.5946},
    "Chennai, Tamil Nadu": {"lat": 13.0827, "lon": 80.2707},
    "Vijayawada, AP": {"lat": 16.5062, "lon": 80.6480}
}

EMERGENCY_KEYWORDS = ["help", "ambulance", "help me", "padipoyanu", "kapadandi", "emergency", "doctor", "bachao", "accident", "madad"]

def load_data():
    try:
        with open("hospitals.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"hospitals": [], "family_contacts": [], "health_tips": [], "medicines": {}}

def check_voice(text):
    return any(w in text.lower() for w in EMERGENCY_KEYWORDS)

def create_emergency_alert(data, reason, city="Guntur, AP", live_lat=None, live_lon=None):
    loc = INDIA_CITIES.get(city, INDIA_CITIES["Guntur, AP"])
    lat = live_lat if live_lat else loc['lat']
    lon = live_lon if live_lon else loc['lon']
    hospitals = [h for h in data.get("hospitals", []) if h.get("city") == city]
    if not hospitals:
        hospitals = data.get("hospitals", [])
    hospitals = sorted(hospitals, key=lambda x: x.get("distance_km", 999))
    nearest = hospitals[0] if hospitals else None
    maps_link = f"https://www.google.com/maps/search/hospital+near+{lat},{lon}"
    ambulance_link = f"https://www.google.com/maps/search/ambulance+near+{lat},{lon}"
    live_link = f"https://www.google.com/maps?q={lat},{lon}"
    msg = f"VOXCARE AI EMERGENCY: {reason} in {city}, India. Live Location: {live_link}. Nearest: {nearest['name'] if nearest else 'Not Found'}. Ambulance: 108. Maps: {maps_link}"
    wa_links = []
    for person in data.get("family_contacts", []):
        phone_clean = person['phone'].replace('+','').replace('-','').replace(' ','')
        wa_links.append({"name": person["name"], "phone": person["phone"], "link": f"https://wa.me/{phone_clean}?text={urllib.parse.quote(msg)}"})
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reason": reason, "city": city,
        "accident_location": f"{city}, India",
        "live_location_link": live_link,
        "nearest_hospital": nearest["name"] if nearest else "Not Found",
        "distance": nearest["distance_km"] if nearest else 0,
        "icu_hospital": nearest["name"] if nearest and nearest.get("icu_beds", 0) > 0 else "No ICU",
        "blood_hospital": nearest["name"] if nearest and nearest.get("blood_bank", {}).get("O+", 0) > 0 else "No O+ Blood",
        "police_station": nearest["police_station"] if nearest else "Dial 100",
        "ambulance_status": nearest["ambulance"] if nearest else "Call 108",
        "doctor_available": nearest.get("doctor_available", "Doctor On Duty") if nearest else "Not Known",
        "op_available": nearest.get("op_available", "OP Available") if nearest else "Not Known",
        "beds_available": nearest.get("beds_available", 10) if nearest else 0,
        "maps_link": maps_link, "ambulance_link": ambulance_link,
        "family_links": wa_links, "family": data.get("family_contacts", [])
    }

def health_assistant(symptom, data, language="English"):
    s = symptom.lower()
    meds = data.get("medicines", {})
    prefix = {"Telugu": "Nee problem ki: ", "Hindi": "Aapki samasya ke liye: ", "English": ""}.get(language, "")
    if "fever" in s or "jwaram" in s or "bukhar" in s:
        return f"{prefix}Fever: Drink more water, rest. Medicine: {meds.get('fever')}. If not reduced in 2 days, visit hospital."
    if "headache" in s or "thalaka" in s or "sir dard" in s:
        return f"{prefix}Headache: Rest, water. Medicine: {meds.get('headache')}"
    if "chest" in s or "gundelo" in s or "seene" in s:
        return "Chest Pain can be EMERGENCY. Press HELP immediately."
    if "sugar" in s or "diabetes" in s or "madhumeham" in s:
        return f"{prefix}Sugar: 30 min walking daily. Medicine: {meds.get('sugar')}"
    if "bp" in s or "pressure" in s:
        return f"{prefix}BP: Reduce salt. Medicine: {meds.get('bp')}"
    if "cold" in s or "jalubu" in s or "sardi" in s:
        return f"{prefix}Cold: Warm water, rest. Medicine: {meds.get('cold')}"
    if "certificate" in s or "report" in s:
        return "Medical Certificate / Report: Take OPD slip + ID proof + old reports to hospital doctor. Govt: Free, Private: Rs.100-500. You get in 1-2 days. For sending report online: Ask hospital for PDF report on WhatsApp / Email, then forward to school / office. Doctor signature + seal must be there."
    if "op" in s or "appointment" in s or "book" in s:
        return "OP Booking from Home: Open hospital link in Emergency tab, call hospital number, or use Google Maps -> Hospital -> Book Appointment. You can book OP without going to hospital."
    return f"{prefix}Rest, water, healthy food. If not reduced, consult doctor. If emergency, press HELP."

def medicine_reminder(medicine, time_str):
    return f"Reminder Set: {medicine} - Take at {time_str}."
