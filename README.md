# Network Scanner

A simple Flask-based web application to scan a local network for new devices using `nmap`.

## Requirements

- Kali Linux (or any Linux with `nmap` installed)
- Python 3.x
- Flask
- `nmap` Python library

## Setup

1. Install system dependencies:

   ```bash
   sudo apt update
   sudo apt install nmap
2. Create and activate a Python virtual environment:
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. Install Python dependencies from requirements.txt:
   ```bash
   pip install -r requirements.txt
4. Run the Flask app with:
   ```bash
   sudo venv/bin/python3 app.py
5. Access the app in your browser at:
   http://<>:5000
   Replace <> with your actual machine IP address.
   
Additional Notes:
Your machine should be connected to the network with a Bridged Adapter (in virtual environments) to scan devices properly.
Ensure you have permission to scan the network.
requirements.txt contains all Python dependencies:
```bash
flask
nmap
gunicorn

