# VoxCare - Voice-based Emergency Healthcare System

VoxCare is a 3-layer emergency system that helps users during accidents, even when they cannot speak or are unconscious. It connects Hospital, Family, and Police in one alert, with live ambulance tracking.

## Problem
During an accident, a user may not be able to type or speak. If they go to a hospital with no ICU bed or blood, time is wasted. At night, with no one around, help may arrive late. Family does not know where the ambulance is.

## Solution - 3 Layer Safety System

**Layer 1 - Voice Mode**
User says "Accident" -> Nearest hospital with ICU bed, ambulance, family + police alert.

**Layer 2 - Silent SOS Mode**
User cannot speak -> Button press triggers SOS. No voice needed.
Sends location to hospital, family, and police.

**Layer 3 - Auto Crash Detection Mode**
User is unconscious / phone is in car -> Accelerometer detects crash.
If no response in 30 seconds, auto SOS is sent.
Pre-crash signal is stored in cloud, so alert survives even if phone is destroyed.

## Ambulance Tracking - Like Food Delivery Tracking
VoxCare shows ambulance live status:
- Ambulance from which hospital
- Distance in KM
- ETA in minutes
- Traffic clearance request to police
- Family notification with ETA

Example: "Ambulance is 2.1 KM away, reaching in approx 6 minutes"

## Why Police Alert?
Police is needed for traffic clearance for ambulance, accident documentation, and FIR support. VoxCare sends accident location to nearest police station along with hospital alert.

## How it works

User Input / Crash Sensor -> Intent / Crash Detection -> Nearest Hospital Search -> Alert to Hospital + Family + Police + Ambulance Tracking

Examples:
- "Accident" -> Emergency Mode, hospital + ambulance + family + police + tracking
- "O+ blood" -> Nearest hospital with O+ blood available
- "Dr Ramesh OP" -> OP booking with token number
- "Ambulance" / "Track Ambulance" -> Live ambulance distance + ETA
- "Police" -> Nearest police station alert

## Features
- 3-layer system: Voice, Silent SOS, Auto Crash Detection
- Distance-based hospital ranking
- ICU bed and ventilator availability check
- Blood bank availability with fallback to next hospital
- Doctor availability check
- OP booking with token management
- Single alert to Hospital, Family, and Police
- Ambulance live tracking with distance + ETA
- Cloud backup for crash signal

## Tech Stack
Python, JSON

## Run

pip install -r requirements.txt
python main.py
python test_voxcare.py

## Future Improvements
- Real voice input using SpeechRecognition
- Real GPS location
- Smartwatch heart-rate integration
- Real-time hospital data API
- Live map view for ambulance tracking
