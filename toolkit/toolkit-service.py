from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

class Scan:
    def __init__(self):
        self.scan_running = False

scan_obj = Scan()

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message":"pong!"})

@app.route('/status', methods=['GET'])
def status():
    if scan_obj.scan_running:
        return jsonify({"scan_running":True})
    else:
        return jsonify({"scan_running":False})

def toggle_global():
    global scan_obj
    if scan_obj.scan_running:
        scan_obj.scan_running = False
    else:
        scan_obj.scan_running = True

@app.route('/wildfire', methods=['POST'])
def wildfire():
    global scan_obj
    if not scan_obj.scan_running:
        data = request.get_json()
        fire_starter = data['fireStarter']
        fire_cloud = data['fireCloud']
        fire_scanner = data['fireScanner']
        fqdn = data.get('fqdn', '')  # Get the FQDN, default to empty string if not provided
        scan_single_domain = data.get('scanSingleDomain', False)  # Get the scanSingleDomain flag

        start_flag, cloud_flag, scan_flag, fqdn_flag, scanSingle_flag  = "", "", "", "", ""
        if fire_starter:
            start_flag = " --start"
        if fire_cloud:
            cloud_flag = " --cloud"
        if fire_scanner:
            scan_flag = " --scan"
        if scan_single_domain:
            fqdn_flag = f" --fqdn {fqdn}"
            scanSingle_flag = f" --scanSingle"

        toggle_global()
        subprocess.run([f"python3 wildfire.py{start_flag}{cloud_flag}{scan_flag}{fqdn_flag}{scanSingle_flag}"], shell=True)
        toggle_global()
        return jsonify({"message": "Done!"})
    else:
        return jsonify({"message": "ERROR: Scan Running..."})

if __name__ == '__main__':
    app.run(debug=True)