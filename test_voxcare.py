# VOXCARE AI - Final Test - Run: python test_voxcare.py
from voxcare import load_data, create_emergency_alert, health_assistant, check_voice, INDIA_CITIES

def test_all():
    print("VOXCARE AI Testing Started...")
    data = load_data()

    # 1. Hospitals Check - 7 Cities, 8 Hospitals
    assert len(data["hospitals"]) == 8, f"Hospitals 8 undali, unnavi: {len(data['hospitals'])}"
    print("PASS 1: 8 Hospitals unnayi")

    # 2. All 7 Cities Check
    cities = set(h["city"] for h in data["hospitals"])
    assert len(cities) == 7, f"7 Cities undali, unnavi: {cities}"
    print("PASS 2: 7 Cities anni unnayi - Guntur, Hyderabad, Delhi, Mumbai, Bengaluru, Chennai, Vijayawada")

    # 3. Mumbai Hospital Check - Chinna Mistake Fix Ayinda?
    mumbai = [h for h in data["hospitals"] if h["city"] == "Mumbai, Maharashtra"]
    assert len(mumbai) == 1 and "Kokilaben" in mumbai[0]["name"]
    print("PASS 3: Mumbai - Kokilaben Hospital undi")

    # 4. Doctor + OP + Beds Check
    for h in data["hospitals"]:
        assert "doctor_available" in h, f"Doctor ledu: {h['name']}"
        assert "op_available" in h, f"OP ledu: {h['name']}"
        assert "beds_available" in h, f"Beds ledu: {h['name']}"
        assert "op_fee" in h, f"OP Fee ledu: {h['name']}"
    print("PASS 4: Prathi hospital ki Doctor + OP + Beds + OP Fee unnayi")

    # 5. Emergency Alert Check - Guntur
    alert = create_emergency_alert(data, "Test Accident", "Guntur, AP")
    assert "Guntur" in alert["nearest_hospital"] or "Guntur" in alert["city"]
    assert "108" in alert["ambulance_status"]
    assert len(alert["family_links"]) == 2
    print(f"PASS 5: Emergency Alert - Nearest: {alert['nearest_hospital']}, Ambulance: {alert['ambulance_status']}")

    # 6. Emergency Alert Check - Mumbai - Wrong City Hospital Ravoddhu
    alert_mumbai = create_emergency_alert(data, "Test Accident", "Mumbai, Maharashtra")
    assert "Mumbai" in alert_mumbai["nearest_hospital"] or "Kokilaben" in alert_mumbai["nearest_hospital"]
    print(f"PASS 6: Mumbai select chesthe Mumbai hospital ye vasthundi: {alert_mumbai['nearest_hospital']}")

    # 7. Voice Check
    assert check_voice("help me") == True
    assert check_voice("hello") == False
    print("PASS 7: Voice Keyword - HELP detect avthundi")

    # 8. Health Assistant Check
    assert "Fever" in health_assistant("fever", data, "English")
    assert "Certificate" in health_assistant("medical certificate", data, "English") or "Report" in health_assistant("medical certificate", data, "English")
    assert "OP Booking" in health_assistant("op booking", data, "English")
    print("PASS 8: Health Assistant - Fever + Certificate + OP Booking anni pani chesthunnayi")

    # 9. India Cities Check
    assert len(INDIA_CITIES) == 7
    print("PASS 9: INDIA_CITIES lo 7 cities unnayi")

    # 10. Family Contacts Check
    assert len(data["family_contacts"]) == 2
    print("PASS 10: 2 Family Members unnaru")

    print("\nALL 10 TESTS PASSED - VOXCARE AI 100% CORRECT")

if __name__ == "__main__":
    test_all()
