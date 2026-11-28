# VOXCARE AI - Automated Verification Suite
# Run: python test_voxcare.py

from voxcare import (
    INDIA_CITIES,
    check_voice,
    create_emergency_alert,
    health_assistant,
    load_data,
    medicine_reminder,
)


def test_all():
    print("VOXCARE AI Testing Started...\n")
    data = load_data()

    # 1. Hospitals Check - India-Wide Dataset
    hospitals = data.get("hospitals", [])
    assert len(hospitals) >= 8, f"Expected at least 8 hospitals, found: {len(hospitals)}"
    print(f"PASS 1: {len(hospitals)} hospitals loaded across India")

    # 2. Core Cities Coverage Check
    cities = {h.get("city", "") for h in hospitals}
    expected_core_cities = {
        "Guntur, AP",
        "Hyderabad, Telangana",
        "Delhi",
        "Mumbai, Maharashtra",
        "Bengaluru, Karnataka",
        "Chennai, Tamil Nadu",
        "Vijayawada, AP",
    }
    missing_cities = expected_core_cities - cities
    assert not missing_cities, f"Missing core cities: {missing_cities}"
    print("PASS 2: All 7 core Indian cities present (Guntur, Hyderabad, Delhi, Mumbai, Bengaluru, Chennai, Vijayawada)")

    # 3. Mumbai Hospital Check
    mumbai = [h for h in hospitals if h.get("city") == "Mumbai, Maharashtra"]
    assert len(mumbai) >= 1 and any("Kokilaben" in h.get("name", "") for h in mumbai), (
        f"Expected Kokilaben Hospital in Mumbai, got: {mumbai}"
    )
    print("PASS 3: Mumbai - Kokilaben Hospital verified")

    # 4. Hospital Readiness Fields Check (Doctor, OP, Beds, OP Fee, ICU, Blood Bank)
    for h in hospitals:
        for field in ("doctor_available", "op_available", "beds_available", "op_fee", "icu_beds", "blood_bank"):
            assert field in h, f"Missing '{field}' in hospital: {h.get('name')}"
    print("PASS 4: Every hospital has Doctor, OP, Beds, OP Fee, ICU, and Blood Bank info")

    # 5. Emergency Alert Check - Guntur
    alert_guntur = create_emergency_alert(data, "Test Accident", "Guntur, AP")
    assert "Guntur" in alert_guntur["nearest_hospital"] or "Guntur" in alert_guntur["city"]
    assert "108" in alert_guntur["ambulance_status"]
    assert len(alert_guntur["family_links"]) == 2
    for key in ("police_link", "icu_beds", "blood_o_plus", "ambulance_eta_mins", "live_location_link"):
        assert key in alert_guntur, f"Missing alert key: {key}"
    print(f"PASS 5: Guntur Emergency Alert - Nearest: {alert_guntur['nearest_hospital']}, ETA: {alert_guntur['ambulance_eta_mins']}m")

    # 6. Emergency Alert Check - Mumbai Isolation
    alert_mumbai = create_emergency_alert(data, "Test Accident", "Mumbai, Maharashtra")
    assert "Mumbai" in alert_mumbai["nearest_hospital"] or "Kokilaben" in alert_mumbai["nearest_hospital"]
    print(f"PASS 6: Mumbai Emergency Alert routed accurately to: {alert_mumbai['nearest_hospital']}")

    # 7. India-Wide Custom City & Live GPS Coordinates Check
    alert_custom = create_emergency_alert(
        data,
        "Highway Jerk Alert",
        "Kochi, Kerala",
        live_lat=9.9312,
        live_lon=76.2673,
    )
    assert "9.9312" in alert_custom["live_location_link"] and "76.2673" in alert_custom["live_location_link"]
    assert alert_custom["city"] == "Kochi, Kerala"
    print("PASS 7: India-wide custom city & live GPS coordinates working accurately")

    # 8. Voice Keyword Detection Check
    assert check_voice("help me") is True
    assert check_voice("accident near highway") is True
    assert check_voice("hello friend") is False
    print("PASS 8: Voice keyword detector accurate")

    # 9. Health Friend & Medicine Reminder Check
    fever_reply = health_assistant("fever", data, "English").lower()
    cert_reply = health_assistant("medical certificate", data, "English").lower()
    op_reply = health_assistant("op booking", data, "English").lower()
    reminder_reply = medicine_reminder("Paracetamol", "8:00 AM")

    assert "fever" in fever_reply
    assert "certificate" in cert_reply or "report" in cert_reply
    assert "op" in op_reply or "appointment" in op_reply
    assert "Paracetamol" in reminder_reply and "8:00 AM" in reminder_reply
    print("PASS 9: Health Friend (Fever, Certificate, OP Booking) & Medicine Reminder verified")

    # 10. INDIA_CITIES & Family Contacts Check
    assert len(INDIA_CITIES) >= 7
    assert len(data.get("family_contacts", [])) == 2
    print(f"PASS 10: {len(INDIA_CITIES)} India cities configured & 2 family contacts ready")

    print("\nALL 10 TEST SUITES PASSED - VOXCARE AI READY FOR DEMO & DEPLOYMENT")


if __name__ == "__main__":
    test_all()
