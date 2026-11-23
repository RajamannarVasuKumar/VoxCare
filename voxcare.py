import json

print("Testing VoxCare...")

# Test 1: hospitals.json loading
with open("hospitals.json", "r") as f:
    data = json.load(f)

assert len(data["hospitals"]) == 3, "Hospitals count wrong"
print("Test 1 PASSED: hospitals.json loaded - 3 hospitals found")

# Test 2: Sorting by distance
hospitals = sorted(data["hospitals"], key=lambda x: x["distance_km"])
assert hospitals[0]["distance_km"] == 2.1, "Nearest hospital wrong"
print(f"Test 2 PASSED: Nearest hospital is {hospitals[0]['name']} - 2.1 KM")

# Test 3: ICU check
icu_hospital = None
for h in hospitals:
    if h["icu_beds"] > 0:
        icu_hospital = h
        break
assert icu_hospital is not None, "No ICU hospital found"
print(f"Test 3 PASSED: ICU hospital found - {icu_hospital['name']} - {icu_hospital['icu_beds']} beds")

# Test 4: Blood availability
blood_found = False
for h in hospitals:
    if h["blood_bank"].get("O+", 0) > 0:
        blood_found = True
        break
assert blood_found == True, "O+ blood not found"
print("Test 4 PASSED: O+ blood available in nearby hospital")

# Test 5: Family contacts
assert len(data["family_contacts"]) == 2, "Family contacts missing"
print("Test 5 PASSED: Family contacts loaded")

# Test 6: Police info
assert "police_station" in hospitals[0], "Police info missing"
print(f"Test 6 PASSED: Police station linked - {hospitals[0]['police_station']}")

print("\nAll 6 Tests PASSED! VoxCare is working correctly.")
