# VOXCARE AI - Emergency System & Personal Health Assistant

India-wide AI-powered voice web app. Works in any city in India. Real Voice + Real GPS Location.

## Problem
During an accident, a person cannot speak properly or unlock their phone.
It takes 5-10 minutes just to call an ambulance, which can be life-threatening.

## Solution - VOXCARE AI
VOXCARE AI sends alerts to Ambulance, Hospital, Police, and Family using only voice.
It acts as a 3rd Person when no one is near.

## Type 1 - Personal Health Assistant - Home Doctor / Friend in Phone
- Any Language: English / Telugu / Hindi - Talk like a friend
- Any Health Problem: Fever, Headache, Chest Pain, Sugar, BP, Cold - Solution + Medicine Info
- Healthcare Tips, Medicine Reminder
- Medical Certificate / Medical Report: How to get, How to send online
- Near & Affordable Hospitals: OP Fee, Doctor Available, Beds, OP Booking from Home
- Upload Medical Report

## Type 2 - Emergency System - 3rd Person When No One Is Near
- Accident Auto-Detection: App asks "Are You OK?" - No reply in 10 sec = Auto Alert
- Real Voice: Speak HELP - Real Mic Input
- Real Location: Live GPS Location + Ambulance Live Location
- Auto Alert: Ambulance 108 + Near Police Station + 2 Family Members via WhatsApp (Free Real Alert)
- Hospital Arrange: Beds, Blood Bank, Doctor Available, OP, ICU - Informed to Hospital
- Near Hospitals + Google Maps

## 3 Layers
1. Voice Mode: When the user says "HELP / Accident", it sends an alert to the nearest ICU hospital.
2. Silent SOS: When the user cannot speak, pressing the SOS button sends an alert.
3. Auto Crash Detection: If the phone detects a crash and there is no response within 10 seconds, it sends an auto SOS.

## Features - Live Demo Example
- Nearest Hospital: 2.1 KM - Guntur Government General Hospital
- ICU Beds: 12, Beds Available: 25, Blood O+: 8
- Police Station: Guntur Arundelpet PS - 1.2 KM
- Ambulance: 108 - Arrives in 5 min - Live Tracking like Swiggy / Zomato
- Doctor: Dr. Kumar - General - Available | OP: Open 9 AM - 1 PM | OP Fee: Rs.0
- SMS / WhatsApp to Family with Live Location + ETA

## Files
- hospitals.json - 8 Hospitals, 7 Cities - Hospitals data
- voxcare.py - All main functions
- main.py - Main file to run
- test_voxcare.py - 10 Tests Passed
- requirements.txt - streamlit
- README.md - Project details
- DEMO.md - Demo Script

## How to Run
streamlit run main.py

## Commands to Try
HELP, Accident, SOS, Crash, Fever, Headache, Sugar, BP, O+ blood, OP booking, Medical Certificate

## Future Work
Twilio Real Auto Call / SMS after API Key + DLT Registration. Currently Free WhatsApp Real Alert is ready.
