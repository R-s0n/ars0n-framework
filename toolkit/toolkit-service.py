from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message":"pong!"})

@app.route('/wildfire', methods=['POST'])
def wildfire():
    data = request.get_json()
    fire_starter = data['fireStarter']
    fire_cloud = data['fireCloud']
    fire_scanner = data['fireScanner']
    start_flag, cloud_flag, scan_flag = "", "", ""
    if fire_starter:
        start_flag = " --start"
    if fire_cloud:
        cloud_flag = " --cloud"
    if fire_scanner:
        scan_flag = " --scan"
    subprocess.run([f"python3 wildfire.py{start_flag}{cloud_flag}{scan_flag}"], shell=True)
    return jsonify({"message":"Done!"})

if __name__ == '__main__':
    app.run(debug=True)