# VoxCare - Demo Script

## Problem
Accident ayinappudu manam matladalemu, phone unlock cheyalemu.
Ambulance ki call cheyadaniki 5-10 mins late avthundi.

## Solution - VoxCare
Voice tho ne Ambulance, Hospital, Police, Family ki alert pampisthundi.

## 3 Layers
1. Voice Mode: "Accident" anagane nearest ICU hospital ki alert
2. Silent SOS: Matladaleni appudu SOS button nokithe alert
3. Auto Crash: Phone crash detect chesi, 30 sec lo response lekapothe auto SOS

## Features
- Nearest Hospital: 2.1 KM - Sri Venkateswara Hospital
- ICU Beds, Blood Bank, Police Station linked
- Ambulance Tracking like Swiggy / Zomato
- Family ku ETA tho SMS

## Files
- hospitals.json - Hospitals data
- voxcare.py - All functions
- main.py - Main file to run
- test_voxcare.py - 6 Tests Passed

## How to Run
python main.py
Commands: accident, sos, crash, O+ blood, Dr Ramesh OP, ambulance
