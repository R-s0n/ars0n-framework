from os import remove
import requests, sys, subprocess, getopt, json, time, math
from datetime import datetime

start = datetime.now()

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
short_options = "d:s:p:t:"
long_options = ["domain=","server=","port=","template="]

get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
home_dir = get_home_dir.stdout.replace("\n", "")

# blacklist = ['token-spray/','iot/',"/technologies/fingerprinthub-web-fingerprints.yaml",
#             'misconfiguration/http-missing-security-headers.yaml',
#             'helpers/','fuzzing/','/ssl/mismatched-ssl.yaml','vulnerabilities/generic/request-based-interaction.yaml']

blacklist = []

for template in blacklist:
    subprocess.run([f"rm -rf {home_dir}/nuclei-templates/{template}"], shell=True)

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except:
    sys.exit(2)

hasDomain = False
hasServer = False
hasPort = False
hasTemplate = False

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
    if current_argument in ("-t", "--template"):
        template = current_value
        hasTemplate = True

if hasDomain is False or hasServer is False or hasPort is False or hasTemplate is False:
    print("[!] USAGE: python3 kindling.py -d [TARGET_FQDN] -s [WAPT_FRAMEWORK_IP] -p [WAPT_FRAMEWORK_PORT] -t [TEMPLATE]")
    sys.exit(2)

get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
home_dir = get_home_dir.stdout.replace("\n", "")

subprocess.run([f'export PATH="$HOME/go/bin:$PATH"; {home_dir}/go/bin/nuclei -update -ut;'], shell=True)

now_start = datetime.now().strftime("%d-%m-%y_%I%p")

start = time.time()

r = requests.post(f'http://{server_ip}:{server_port}/api/auto', data={'fqdn':fqdn})
thisFqdn = r.json()

httprobe_arr = thisFqdn['recon']['subdomains']['httprobe']
masscan_arr = thisFqdn['recon']['subdomains']['masscanLive']

urls = httprobe_arr + masscan_arr
url_str = ""

for url in urls:
    url_str += f"{url}\n"

f = open("/tmp/urls.txt", "w")
f.write(url_str)
f.close()

now = datetime.now().strftime("%d-%m-%y_%I%p")

subprocess.run([f"{home_dir}/go/bin/nuclei -t {template} -l /tmp/urls.txt -es info -fhr -sb --headless -o /tmp/{fqdn}-{now}.json -json"], shell=True)

f = open(f"/tmp/{fqdn}-{now}.json")
results = f.read().split("\n")
data = []
counter = 0
for result in results:
    counter += 1
    try:
        if len(result) < 5:
            i = results.index(result)
            del results[i]
            continue
        json_result = json.loads(result)
        data.append(json_result)
    except Exception as e:
        print(f"[!] Failed to load result on line {counter}!  Skipping...")
        print(f"[!] Excpetion: {e}")
res = requests.post(f"http://{server_ip}:{server_port}/api/auto", data={"fqdn":fqdn})
thisFqdn = res.json()
thisFqdn['vulns'] = data
requests.post(f'http://{server_ip}:{server_port}/api/auto/update', json=thisFqdn, headers={'Content-type':'application/json'})
info_counter = 0
non_info_counter = 0
for result in data:
    if result['info']['severity'] == 'info':
        info_counter += 1
        result['impactful'] = False
    else :
        non_info_counter += 1
        result['impactful'] = True
end = time.time()
runtime_seconds = math.floor(end - start)
runtime_minutes = math.floor(runtime_seconds / 60)
target_count = len(urls)
if non_info_counter > 0:
    message_json = {'text':f'Nuclei Scan Completed!\n\nResults:\nWeb Servers Scanned: {target_count}\nRood/Seed Targeted: {fqdn}\nTemplate Category: {template}\nImpactful Results: {non_info_counter}\nInformational Results: {info_counter}\nScan Time: {runtime_minutes} minutes\nReport Location: {home_dir}/Reports/{template}-{now}.json\n\nNothing wrong with a little Spray and Pray!!  :pray:','username':'Vuln Disco Box','icon_emoji':':dart:'}
    f = open(f'{home_dir}/.keys/slack_web_hook')
    token = f.read()
    slack_auto = requests.post(f'https://hooks.slack.com/services/{token}', json=message_json)     
