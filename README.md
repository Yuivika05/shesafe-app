🛡️ SheSafe — Crisis Response & Evidence Vault
A personal safety web platform combining live route monitoring, hands-free distress detection, and tamper-evident evidence preservation — built on in-browser hardware APIs (GPS, microphone) and cryptographic hashing (SHA-256, HMAC-SHA256, PBKDF2).

⚠️ SheSafe is a supplementary safety tool, not a substitute for emergency services. In India, call 112 (emergency), 181 (women's helpline), or 1930 (cybercrime).

Features
Feature	Description
🚨	Emergency SOS	Captures live GPS coordinates and generates one-tap dispatch links for SMS and WhatsApp.
🗺️	Route Geofence Watchdog	Monitors travel in real time and alerts if the vehicle drifts away from the intended destination.
🎙️	Acoustic Distress Sentinel	Detects high-decibel audio spikes (screaming, struggle noises) hands-free via the microphone.
🔐	Tamper-Evident Evidence Vault	Cryptographically seals incident transcripts and media to support Section 65B electronic-record admissibility.
📄	Automated Police Complaint	Generates a downloadable Cyber Cell complaint PDF with embedded verification digests.
🧮	Stealth Calculator Mode	One-tap toggle that disguises the platform as a working numeric calculator.
Algorithms: Haversine formula (route deviation) · PBKDF2 with 100,000 salted iterations (vault password hardening) · HMAC-SHA256 notarization (tamper detection) · audio spectral peak sampling (distress detection).

Tech Stack
Python 3 · JavaScript · Gradio Blocks · Web Audio API · HTML5 Geolocation API · PBKDF2 / HMAC-SHA256 / SHA-256 · ReportLab · python-dotenv · JSON storage

Quick Start
Bash

git clone https://github.com/Yuivika05/shesafe-app.git
cd shesafe-app
pip install gradio pillow reportlab python-dotenv
python -c "import secrets; print('SECRET_SALT=' + secrets.token_hex(32))" >> .env
python app.py        # or run SheSafe.ipynb
⚠️ Never commit .env or reuse a salt from documentation — a guessable salt weakens every vault password derived from it.

ℹ️ Geolocation and microphone access require a secure context: run on localhost or HTTPS, and grant the browser prompts.

Legal Framework Reference
Information Technology Act, 2000 — § 66D (cheating by personation), § 66E (privacy violation), § 67 / § 67A (obscene electronic content)
Bharatiya Nyaya Sanhita, 2023 — stalking, criminal intimidation, and harassment provisions
Indian Evidence Act, 1872, § 65B — electronic-record admissibility (successor: § 63, Bharatiya Sakshya Adhiniyam, 2023)
SheSafe produces the digests and audit trails such certificates can reference; formal admissibility additionally requires a certificate in the prescribed form — consult a lawyer for specifics.
