# VoxCare - Demo Script

## Problem
During an accident, a person cannot speak properly or unlock their phone.
It takes 5-10 minutes just to call an ambulance, which can be life-threatening.

## Solution - VoxCare
VoxCare sends alerts to Ambulance, Hospital, Police, and Family using only voice.

## 3 Layers
1. Voice Mode: When the user says "Accident", it sends an alert to the nearest ICU hospital.
2. Silent SOS: When the user cannot speak, pressing the SOS button sends an alert.
3. Auto Crash Detection: If the phone detects a crash and there is no response within 30 seconds, it sends an auto SOS.

## Features
- Nearest Hospital: 2.1 KM - Sri Venkateswara Hospital
- ICU Beds, Blood Bank, Police Station linked
- Ambulance Tracking like Swiggy / Zomato
- SMS to Family with ETA

## Files
- hospitals.json - Hospitals data
- voxcare.py - All main functions
- main.py - Main file to run
- test_voxcare.py - 6 Tests Passed

## How to Run
python main.py

## Commands to Try
accident, sos, crash, O+ blood, Dr Ramesh OP, ambulance
