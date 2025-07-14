from flask import Flask, jsonify, render_template
import os
import socket
import subprocess

app = Flask(__name__)

KNOWN_DEVICES_FILE = "known_devices.txt"

@app.route('/')
def index():
    return render_template('index.html')

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_subnet(ip):
    parts = ip.split(".")
    parts[-1] = "0/24"
    return ".".join(parts)

def run_nmap(subnet):
    try:
        output = subprocess.check_output(["nmap", "-sn", subnet], text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error running nmap: {e}"

def get_devices(nmap_output):
    lines = nmap_output.split("\n")
    devices = []
    for i in range(len(lines)):
        if "Nmap scan report for" in lines[i]:
            ip = lines[i].split()[-1]
            mac = ""
            if i + 2 < len(lines) and "MAC Address" in lines[i+2]:
                mac = lines[i+2].split()[2]
            devices.append((ip, mac))
    return devices

def load_known_devices():
    if not os.path.exists(KNOWN_DEVICES_FILE):
        return set()
    with open(KNOWN_DEVICES_FILE, "r") as f:
        return set([line.strip() for line in f.readlines()])

def save_known_devices(devices):
    with open(KNOWN_DEVICES_FILE, "w") as f:
        for ip, mac in devices:
            f.write(f"{ip} {mac}\n")

def check_for_new(devices, known):
    new_devices = []
    for ip, mac in devices:
        entry = f"{ip} {mac}"
        if entry not in known:
            new_devices.append(entry)
    return new_devices

@app.route('/scan', methods=['POST'])
def scan_network():
    try:
        local_ip = get_local_ip()
        subnet = get_subnet(local_ip)
        scan_result = run_nmap(subnet)
        devices = get_devices(scan_result)
        known = load_known_devices()
        new = check_for_new(devices, known)
        save_known_devices(devices)
        return jsonify({
            'local_ip': local_ip,
            'subnet': subnet,
            'new_devices': new
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
