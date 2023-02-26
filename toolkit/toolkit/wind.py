# Find which IP/Port combinations (from firewood.py) are hosting a web server
# Automated - 24 hrs
# Runtime - 60 min avg

import requests, sys, subprocess, getopt, json, time, math
from datetime import datetime

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
short_options = "d:s:p:"
long_options = ["domain=","server=","port="]

start = time.time()

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except:
    sys.exit(2)

hasDomain = False
hasServer = False
hasPort = False

for current_argument, current_value in arguments:
    if current_argument in ("-d", "--domain"):
        fqdn = current_value
        hasDomain = True
    if current_argument in ("-s", "--server"):
        server_ip = current_value
        hasServer = True
    if current_argument in ("-p", "--port"):
        server_port = current_value
        hasPort = True

get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
home_dir = get_home_dir.stdout.replace("\n", "")

r = requests.post(f'http://{server_ip}:{server_port}/api/auto', data={'fqdn':fqdn})
thisFqdn = r.json()

server_data_arr = thisFqdn['recon']['subdomains']['masscan']
server_data_str = ""

for server in server_data_arr:
    server_data_str += f"{server}\n"

f = open("/tmp/masscan_httprobe.tmp", "w")
f.write(server_data_str)
f.close()

live_server_arr = []

print(f"[-] Running Httprobe against masscan results...")
connect = subprocess.run([f"cat /tmp/masscan_httprobe.tmp | {home_dir}/go/bin/httprobe -t 30000 -c 50"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
print(f"[+] Httprobe completed successfully!")
temp_arr = connect.stdout.split("\n")
for each in temp_arr:   
    if len(each) > 5:
        live_server_arr.append(each)

final_arr = []
for server in live_server_arr:
    if server not in final_arr:
        final_arr.append(server)

print(f"[-] Updating database...")
r = requests.post(f'http://{server_ip}:{server_port}/api/auto', data={'fqdn':fqdn})
thisFqdn = r.json()
thisFqdn['recon']['subdomains']['masscanLive'] = final_arr
r = requests.post(f'http://{server_ip}:{server_port}/api/auto/update', json=thisFqdn, headers={'Content-type':'application/json'})


directory_check = subprocess.run([f"ls {home_dir}/Reports"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
if directory_check.returncode == 0:
    print("[+] Identified Reports directory")
else:
    print("[!] Could not locate Reports directory -- Creating now...")
    cloning = subprocess.run([f"mkdir {home_dir}/Reports"], stdout=subprocess.DEVNULL, shell=True)
    print("[+] Reports directory successfully created")

eyewitness_check = httprobe_check = subprocess.run([f"ls {home_dir}/Tools/EyeWitness"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
if httprobe_check.returncode == 0:
    print("[+] EyeWitness is already installed")
else :
    print("[!] EyeWitness is NOT already installed -- Installing now...")
    cloning = subprocess.run([f"cd {home_dir}/Tools; git clone https://github.com/FortyNorthSecurity/EyeWitness.git;  cd EyeWitness/Python/setup/;  sudo ./setup.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    print("[+] EyeWitness successfully installed!")

server_string = ""
for server in final_arr:
    server_string += f"{server}\n"
f = open("/tmp/httprobe_masscan_results.tmp", "w")
f.write(server_string)
f.close()
now = datetime.now().strftime("%d-%m-%y_%I%p")
print(f"[-] Running EyeWitness report against {fqdn} httprobe results...")
subprocess.run([f"cd {home_dir}/Tools/EyeWitness/Python; ./EyeWitness.py -f /tmp/httprobe_masscan_results.tmp -d {home_dir}/Reports/EyeWitness_wind_{fqdn}_{now} --no-prompt --jitter 5 --timeout 10"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
print(f"[+] EyeWitness report complete!")

end = time.time()
runtime_seconds = math.floor(end - start)
runtime_minutes = math.floor(runtime_seconds / 60)

if r.status_code == 200:
    print(f"[+] Wind.py completed successfully in {runtime_minutes} minutes!")
else:
    print("[!] Wind.py did NOT complete successfully!")