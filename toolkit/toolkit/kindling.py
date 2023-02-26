# Find live servers and run EyeWitness report
# Automated - 6 hrs
# Runtime - 200 min avg

import requests, sys, subprocess, getopt, json, time, math
from datetime import datetime

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
short_options = "d:s:p:"
long_options = ["domain=","server=","port="]

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

if hasDomain is False or hasServer is False or hasPort is False:
    print("[!] USAGE: python3 kindling.py -d [TARGET_FQDN] -s [WAPT_FRAMEWORK_IP] -p [WAPT_FRAMEWORK_PORT]")
    sys.exit(2)

start = time.time()

get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
home_dir = get_home_dir.stdout.replace("\n", "")

r = requests.post(f'http://{server_ip}:{server_port}/api/auto', data={'fqdn':fqdn})
thisFqdn = r.json()

subdomainArr = thisFqdn['recon']['subdomains']['consolidated']

go_check = subprocess.run(["go version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
if go_check.returncode == 0:
    print("[+] Go is installed")
else :
    print("[!] Go is NOT installed -- Installing now...")
    cloning = subprocess.run([f"sudo apt-get install -y golang-go; apt-get install -y gccgo-go; mkdir {home_dir}/go;"], stdout=subprocess.DEVNULL, shell=True)
    print("[+] Go was successfully installed")

try:
    httprobe_check = subprocess.run([f"{home_dir}/go/bin/httprobe -h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    if httprobe_check.returncode == 0:
        print("[+] Httprobe is already installed")
    else :
        print("[!] Httprobe is NOT already installed -- Installing now...")
        cloning = subprocess.run(["go install -v github.com/tomnomnom/httprobe@latest"], stdout=subprocess.DEVNULL, shell=True)
        print("[+] Httprobe successfully installed!")
    print(f"[-] Running Httprobe against {fqdn}...")
    subdomainStr = ""
    for subdomain in subdomainArr:
        subdomainStr += f"{subdomain}\n"
    f = open("/tmp/consolidated_list.tmp", "w")
    f.write(subdomainStr)
    f.close()
    httprobe_results = subprocess.run([f"cat /tmp/consolidated_list.tmp | {home_dir}/go/bin/httprobe -t 20000 -c 50 -p http:8080 -p http:8000 -p http:8008 -p https:8443 -p https:44300 -p https:44301"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    r = requests.post(f'http://{server_ip}:{server_port}/api/auto', data={'fqdn':fqdn})
    thisFqdn = r.json()
    httprobe = httprobe_results.stdout.split("\n")
    previous_httprobe = thisFqdn['recon']['subdomains']['httprobe']
    httprobeAdded = []
    httprobeRemoved = []
    for subdomain in httprobe:
        if subdomain not in previous_httprobe:
            httprobeAdded.append(subdomain)
    for subdomain in previous_httprobe:
        if subdomain not in httprobe:
            httprobeRemoved.append(subdomain)
    thisFqdn['recon']['subdomains']['httprobe'] = httprobe
    thisFqdn['recon']['subdomains']['httprobeAdded'] = httprobeAdded
    thisFqdn['recon']['subdomains']['httprobeRemoved'] = httprobeRemoved
    print("[+] Httprobe completed successfully!")
except:
    print("[!] Httprobe module did NOT complete successfully -- skipping...")

subprocess.run(["rm /tmp/consolidated_list.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
# Send new fqdn object
r = requests.post(f'http://{server_ip}:{server_port}/api/auto/update', json=thisFqdn, headers={'Content-type':'application/json'})

directory_check = subprocess.run([f"ls {home_dir}/Reports"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
if directory_check.returncode == 0:
    print("[+] Identified Reports directory")
else:
    print("[!] Could not locate Reports directory -- Creating now...")
    cloning = subprocess.run([f"mkdir {home_dir}/Reports"], stdout=subprocess.DEVNULL, shell=True)
    print("[+] Reports directory successfully created")

# eyewitness_check = httprobe_check = subprocess.run([f"ls {home_dir}/Tools/EyeWitness"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
# if httprobe_check.returncode == 0:
#     print("[+] EyeWitness is already installed")
# else :
#     print("[!] EyeWitness is NOT already installed -- Installing now...")
#     cloning = subprocess.run([f"cd {home_dir}/Tools; git clone https://github.com/FortyNorthSecurity/EyeWitness.git;  cd EyeWitness/Python/setup/;  sudo ./setup.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
#     print("[+] EyeWitness successfully installed!")
# httprobe_string = ""
# for subdomain in httprobe:
#     httprobe_string += f"{subdomain}\n"
# f = open("/tmp/httprobe_results.tmp", "w")
# f.write(httprobe_string)
# f.close()
# now = datetime.now().strftime("%d-%m-%y_%I%p")
# print(f"[-] Running EyeWitness report against {fqdn} httprobe results...")
# subprocess.run([f"rm -rf {home_dir}/Reports/EyeWitness_kindling_{fqdn}_*"], shell=True)
# subprocess.run([f"cd {home_dir}/Tools/EyeWitness/Python; ./EyeWitness.py -f /tmp/httprobe_results.tmp -d {home_dir}/Reports/EyeWitness_kindling_{fqdn}_{now} --no-prompt --jitter 5 --timeout 10"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
# print(f"[+] EyeWitness report complete!")
print(f"[-] Sending notification through Slack...")
end = time.time()
runtime_seconds = math.floor(end - start)
runtime_minutes = math.floor(runtime_seconds / 60)
message_urls_string = ""
length = len(thisFqdn['recon']['subdomains']['httprobeAdded'])
if length > 10:
    message_json = {'text':f'kindling.py (live server probe) completed successfully in {runtime_minutes} minutes!  This scan of {fqdn} discovered that {length} URLs went live in the last 6 hours!\nHappy Hunting :)','username':'Recon Box','icon_emoji':':eyes:'}
else:
    for url in thisFqdn['recon']['subdomains']['httprobeAdded']:
        message_urls_string += f"{url}\n"
    message_json = {'text':f'kindling.py (live server probe) completed successfully in {runtime_minutes} minutes!  This scan of {fqdn} discovered the following URLs went live in the last 6 hours:\n\n{message_urls_string}\nHappy Hunting :)','username':'Recon Box','icon_emoji':':eyes:'}
f = open(f'{home_dir}/.keys/slack_web_hook')
token = f.read()
slack_auto = requests.post(f'https://hooks.slack.com/services/{token}', json=message_json)

print(f"[+] Kindling.py completed successfully in {runtime_minutes} minutes!")