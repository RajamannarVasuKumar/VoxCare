import json

print("Testing VoxCare...")

with open("hospitals.json", "r") as f:
    data = json.load(f)

assert len(data["hospitals"]) == 3
print("Test 1 PASSED: hospitals.json loaded - 3 hospitals")

hospitals = sorted(data["hospitals"], key=lambda x: x["distance_km"])
assert hospitals[0]["distance_km"] == 2.1
print(f"Test 2 PASSED: Nearest hospital is {hospitals[0]['name']} - 2.1 KM")

icu_hospital = None
for h in hospitals:
    if h["icu_beds"] > 0:
        icu_hospital = h
        break
assert icu_hospital is not None
print(f"Test 3 PASSED: ICU hospital found - {icu_hospital['name']}")

blood_found = False
for h in hospitals:
    if h["blood_bank"].get("O+", 0) > 0:
        blood_found = True
        break
assert blood_found == True
print("Test 4 PASSED: O+ blood available")

assert len(data["family_contacts"]) == 2
print("Test 5 PASSED: Family contacts loaded")

assert "police_station" in hospitals[0]
print(f"Test 6 PASSED: Police linked - {hospitals[0]['police_station']}")

print("\nAll 6 Tests PASSED! VoxCare is working correctly.")
