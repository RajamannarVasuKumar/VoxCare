# VOXCARE AI - Emergency System & Personal Health Assistant

India-wide AI-powered voice and text web application designed to work across cities and states in India with live GPS location links, hospital readiness details, and a friendly health assistant.

> **Safety Note:** Official emergency helplines (**108** for ambulance, **100 / 112** for police/emergency) are always primary in real-world emergencies. VoxCare AI acts as a smart assistive coordination and communication layer.

## Problem
During a sudden road accident or medical emergency, a person may struggle to speak clearly, unlock their phone, or coordinate multiple contacts while every minute counts.

## Solution - VOXCARE AI
VOXCARE AI combines **Health Friend** guidance and **3rd-Person Emergency Coordination** in a zero-cost web interface:
- Supports **Voice + Screen Text** so users can both speak and read clearly.
- Works **India-wide** with preset Indian cities, custom city/town input, and optional live GPS coordinates (`lat`, `lon`).
- Prepares instant Google Maps links and WhatsApp family alert links along with hospital ICU, blood bank (`O+`), bed, OP, and police station details.

## Mode 1 - Health Friend (Voice + Text)
- **Friendly Conversation:** Ask health questions and receive both spoken browser voice-over and clear text on screen.
- **Broad Health Topics:** Fever, headache, chest pain warning, blood sugar, BP, cold, general wellness, daily health tips, and medicine reminders.
- **Practical Guidance:** Step-by-step guidance on medical certificates/reports, online sharing tips, OP booking, and report upload.

## Mode 2 - 3rd-Person Emergency & Crash Guardian
- **1-Click SOS:** Immediate emergency alert card with live GPS location link, hospital/ambulance/police map links, Medical ID summary, and WhatsApp family alert links.
- **10-Second Crash / Consciousness Check:** Simulates a sudden crash/jerk with a 10-second `"Are you okay?"` check before triggering unconscious emergency mode.
- **Voice Input & Keyword Check:** Record voice via mic or type emergency messages (`HELP`, `Accident`, etc.) with keyword detection.
- **Ambulance Live Tracker (For Conscious Victim):** Shows dispatch status, estimated arrival time (ETA), and route progress bar.

## Project Files
- `main.py` - Streamlit UI, voice-over synthesis, 10-second crash check, emergency alert view, and Health Friend interface
- `voxcare.py` - Coordinate resolution, emergency alert builder, keyword checker, medicine reminders, and Gemini + rule-based health assistant
- `hospitals.json` - India-wide hospital readiness data, ambulance ETA, Medical ID info, family contacts, health tips, and medicine notes
- `test_voxcare.py` - Automated verification script (`python test_voxcare.py`)
- `requirements.txt` - Python dependencies (`streamlit`, optional `google-genai`)
- `Dockerfile` - Container configuration for Streamlit hosting (`port 8501`)
- `README.md` - Project documentation
- `DEMO.md` - Live walkthrough script

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run main.py
