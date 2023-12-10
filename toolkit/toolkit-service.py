from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import subprocess
import psutil
import os
import signal

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
CORS(app)

class Scan:
    def __init__(self):
        self.scan_running = False
        self.scan_step = 0
        self.scan_complete = 0
        self.scan_step_name = "Not Running"

scan_obj = Scan()

def start_scan(fire_starter, fire_cloud, fire_scanner):
    global scan_obj
    scan_obj.scan_running = True
    scan_obj.scan_step = 1
    scan_obj.scan_complete = 1
    if fire_starter:
        scan_obj.scan_complete = scan_obj.scan_complete + 11
    if fire_cloud:
        scan_obj.scan_complete = scan_obj.scan_complete + 6
    if fire_scanner:
        scan_obj.scan_complete = scan_obj.scan_complete + 10
    scan_obj.scan_step_name = "Starting..."

def stop_scan():
    global scan_obj
    scan_obj.scan_running = False
    scan_obj.scan_step = 0
    scan_obj.scan_complete = 0
    scan_obj.scan_step_name = "Not Running"

def cancel_subprocesses():
    current_pid = os.getpid()
    all_processes = psutil.process_iter(attrs=['pid', 'ppid', 'cmdline'])
    for process in all_processes:
        pid = process.info['pid']
        ppid = process.info['ppid']
        cmdline = process.info['cmdline']
        if ppid == current_pid and pid != current_pid:
            print(f"Terminating subprocess {pid}: {' '.join(cmdline)}")
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                print(f"Process {pid} not found.")

@app.route('/terminate-subprocesses', methods=['GET'])
def terminate_subprocesses():
    try:
        cancel_subprocesses()
        return jsonify({'message': 'Subprocesses terminated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message":"pong!"})

@app.route('/status', methods=['GET'])
def status():
    global scan_obj
    if scan_obj.scan_running:
        return jsonify({
            "scan_running":True,
            "scan_step":scan_obj.scan_step,
            "scan_complete":scan_obj.scan_complete,
            "scan_step_name":scan_obj.scan_step_name
            })
    else:
        return jsonify({
            "scan_running":False,
            "scan_step":scan_obj.scan_step,
            "scan_complete":scan_obj.scan_complete,
            "scan_step_name":scan_obj.scan_step_name
            })
    
@app.route('/update-scan', methods=['POST'])
def update_scan():
    global scan_obj
    if scan_obj.scan_running:
        data = request.get_json()
        scan_obj.scan_step += 1
        scan_obj.scan_step_name = data['stepName']
        return jsonify({
                "scan_running":scan_obj.scan_running,
                "scan_step":scan_obj.scan_step,
                "scan_step_name":scan_obj.scan_step_name
                })
    else:
        return jsonify({"message": "ERROR: Scan Not Currently Running..."})

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

        start_scan(fire_starter, fire_cloud, fire_scanner)
        subprocess.run([f"python3 wildfire.py{start_flag}{cloud_flag}{scan_flag}{fqdn_flag}{scanSingle_flag}"], shell=True)
        stop_scan()
        return jsonify({"message": "Done!"})
    else:
        return jsonify({"message": "ERROR: Scan Running..."})

if __name__ == '__main__':
    app.run(debug=True)