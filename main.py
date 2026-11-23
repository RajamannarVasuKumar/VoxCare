import json
import time

# Load hospitals data
with open("hospitals.json", "r") as f:
    data = json.load(f)

hospitals = sorted(data["hospitals"], key=lambda x: x["distance_km"])
family = data["family_contacts"]

def send_alert(hospital, message):
    print("\n--- ALERT SENT ---")
    print(f"To Hospital: {hospital['name']}")
    print(f"To Police: {hospital['police_station']} ({hospital['police_distance_km']} KM away)")
    for person in family:
        print(f"To Family: {person['name']} - {person['phone']}")
    print(f"Message: {message}")
    print("-----------------")

def track_ambulance(hospital):
    print("\n--- AMBULANCE TRACKING (Like Food Delivery) ---")
    print(f"Ambulance from: {hospital['name']}")
    print(f"Distance: {hospital['distance_km']} KM")
    eta = int(hospital['distance_km'] * 3)
    print(f"ETA: approx {eta} minutes")
    print("Status: Ambulance started -> On the way -> Reaching soon")
    print("Police requested for traffic clearance.")
    print("Family notified with ETA.")

def emergency_mode():
    print("\n!!! EMERGENCY MODE ACTIVATED !!!")
    print("User said: Accident")
    # Find nearest hospital WITH ICU bed
    selected = None
    for h in hospitals:
        if h["icu_beds"] > 0 and h["ambulance_available"]:
            selected = h
            break
    if not selected:
        selected = hospitals[0]
        print("No ICU bed nearby. Going to nearest hospital as fallback.")

    print(f"\nNearest Hospital with ICU: {selected['name']}")
    print(f"Distance: {selected['distance_km']} KM")
    print(f"ICU Beds Available: {selected['icu_beds']}")
    print(f"Ventilators: {selected['ventilators']}")

    send_alert(selected, "EMERGENCY: Accident at user location. Need ICU + Ambulance immediately.")
    track_ambulance(selected)

def silent_sos():
    print("\n!!! SILENT SOS ACTIVATED !!!")
    print("User pressed SOS button. Cannot speak.")
    selected = hospitals[0]
    print(f"Nearest Hospital: {selected['name']} - {selected['distance_km']} KM")
    send_alert(selected, "SILENT SOS: User cannot speak. Send ambulance immediately to location.")
    track_ambulance(selected)

def crash_detection():
    print("\n!!! AUTO CRASH DETECTION !!!")
    print("Accelerometer detected heavy crash.")
    print("Phone may be damaged. Pre-crash signal saved to Cloud.")
    print("Waiting 30 seconds for user response...")
    time.sleep(2)  # Demo lo 2 sec, real lo 30 sec
    print("No response from user.")
    print("Auto SOS triggered - User may be unconscious.")
    selected = hospitals[0]
    send_alert(selected, "AUTO CRASH: User unconscious. Crash detected. Send ambulance + Police.")
    track_ambulance(selected)

def blood_search(blood_group):
    print(f"\nSearching for Blood Group: {blood_group}")
    for h in hospitals:
        available = h["blood_bank"].get(blood_group, 0)
        if available > 0:
            print(f"Found! {h['name']} - {available} units available - {h['distance_km']} KM away")
            send_alert(h, f"Blood Required: {blood_group}. Please keep ready.")
            return
    print("Not found in nearby hospitals. Checking next city hospitals...")

def op_booking(doctor_name):
    print(f"\nSearching Doctor: {doctor_name}")
    for h in hospitals:
        for doc in h["doctors"]:
            if doctor_name.lower() in doc["name"].lower():
                if doc["op_available"]:
                    print(f"Found! {doc['name']} at {h['name']}")
                    print(f"Speciality: {doc['speciality']}")
                    print(f"Your Token Number: {doc['token']}")
                    print("OP Booked Successfully.")
                    return
                else:
                    print(f"{doc['name']} is NOT available today.")
                    return
    print("Doctor not found.")

def main():
    print("="*50)
    print("VoxCare - Voice-based Emergency Healthcare System")
    print("3-Layer System: Voice | Silent SOS | Auto Crash")
    print("="*50)
    print("\nCommands: accident | sos | crash | O+ blood | Dr Ramesh OP | ambulance | exit")

    while True:
        user_input = input("\nVoxCare > ").lower().strip()

        if user_input == "exit":
            print("Stay Safe. VoxCare closed.")
            break
        elif "accident" in user_input:
            emergency_mode()
        elif "sos" in user_input:
            silent_sos()
        elif "crash" in user_input:
            crash_detection()
        elif "blood" in user_input or "o+" in user_input or "o-" in user_input or "a+" in user_input or "b+" in user_input:
            # Extract blood group
            for bg in ["o+", "o-", "a+", "a-", "b+", "b-", "ab+", "ab-"]:
                if bg in user_input:
                    blood_search(bg.upper())
                    break
            else:
                print("Please say like: O+ blood")
        elif "dr" in user_input or "doctor" in user_input:
            op_booking(user_input)
        elif "ambulance" in user_input or "track" in user_input:
            track_ambulance(hospitals[0])
        elif "police" in user_input:
            h = hospitals[0]
            print(f"Nearest Police: {h['police_station']} - {h['police_distance_km']} KM")
        else:
            print("Try: accident, sos, crash, O+ blood, Dr Ramesh OP, ambulance")

if __name__ == "__main__":
    main()
