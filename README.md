# VOXCARE AI — India-Wide Emergency Guardian & Voice Health Friend

**VOXCARE AI** is a zero-cost, India-wide web application built with **Streamlit** that pairs a conversational **Health Friend** (voice + screen text) with a **3rd-Person Emergency & Crash Guardian** supporting live GPS links, hospital readiness details, and instant family alert dispatch across Indian cities.

> **Safety Notice:** Official emergency helplines (**108** for ambulance, **100 / 112** for police and emergency response) are always primary in real-world emergencies. VOXCARE AI serves as an assistive coordination and communication layer.

### Live Demo
- **Web App:** [Open VOXCARE AI Live](https://voxcare-ai-9wenxcfbdg7eqshbhb6dbm.streamlit.app/)

---

## Core Capabilities

### 1. Health Friend (Voice + Screen Text)
- **Dual-Channel Output:** Delivers clear screen text alongside browser speech synthesis (`window.speechSynthesis`) for hands-free listening.
- **Everyday Health Guidance:** Covers common concerns (fever, headache, chest pain warning signs, blood sugar, BP, cold), general wellness tips, and medicine reminders.
- **Practical Workflows:** Guides users on obtaining and sharing medical certificates/reports, booking outpatient (OP) appointments, and reviewing uploaded reports.
- **Resilient AI Architecture:** Uses Google Gemini (`gemini-2.5-flash` via `google-genai`) when `GEMINI_API_KEY` is configured, with an automatic rule-based fallback so core guidance remains available without interruption.

### 2. 3rd-Person Emergency & Crash Guardian
- **1-Click SOS:** Immediately generates a live GPS Google Maps link (`https://www.google.com/maps?q=...`), hospital/ambulance/police map searches, Medical ID summary, and pre-filled WhatsApp alert links for family contacts.
- **10-Second Crash / Consciousness Check:** Simulates a sudden vehicle impact/jerk with a 10-second `"Are you okay?"` response window before escalating to unconscious emergency mode.
- **Voice Input & Keyword Detection:** Supports microphone audio capture, text input, and emergency keyword detection (`HELP`, `Accident`, `SOS`, etc.).
- **Ambulance Live Tracker (Conscious Victim View):** Displays dispatch status, estimated arrival time (ETA), and route progress.
- **India-Wide Coverage:** Works with preset Indian cities, custom city/town entry across India, and optional live latitude/longitude coordinates.

---

## Repository Structure

| File | Responsibility |
| :--- | :--- |
| `main.py` | Streamlit interface, voice synthesis, 10s crash check, emergency dispatch card, and Health Friend UI |
| `voxcare.py` | Coordinate resolution, emergency alert builder, voice keyword check, medicine reminders, and Gemini + fallback assistant |
| `hospitals.json` | India-wide hospital readiness records (ICU, O+ blood bank, beds, OP status/fee), ambulance ETA, Medical ID, contacts, tips, and medicines |
| `test_voxcare.py` | Automated test suite verifying data integrity, city isolation, GPS coordinates, voice keywords, and health responses |
| `requirements.txt` | Python dependencies (`streamlit`, `google-genai`) |
| `Dockerfile` | Container build and healthcheck setup on port `8501` |
| `README.md` | Project overview, architecture, and setup guide |
| `DEMO.md` | Live walkthrough and hackathon/FDE demonstration guide |

---

## Quick Start

### Run Locally
```bash
pip install -r requirements.txt
streamlit run main.py
