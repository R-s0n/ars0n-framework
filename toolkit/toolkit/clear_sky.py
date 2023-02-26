# Scan Cloud Ranges Proactively
# One-off Scan

import requests, sys, subprocess, getopt, json
from datetime import datetime

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
short_options = "d:s:p:u"
long_options = ["domain=","server=","port=", "update"]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except:
    sys.exit(2)

hasDomain = False
hasServer = False
hasPort = False
updateMode = False

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
    if current_argument in ("-u", "--update"):
        updateMode = True


get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
home_dir = get_home_dir.stdout.replace("\n", "")

print(f"[+] Running ClearSky against {fqdn}!")

if updateMode:
    print("[-] Checking for AWS IP Range JSON...")
    document_check = subprocess.run([f"ls {home_dir}/Wordlists/aws-ip-ranges.json"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, shell=True)
    if document_check.returncode == 0:
        print("[+] AWS IP Range JSON Identified!")
    else:
        print("[!] Could not locate AWS IP Range JSON -- Downloading now...")
        subprocess.run([f"wget -O {home_dir}/Wordlists/aws-ip-ranges.json https://ip-ranges.amazonaws.com/ip-ranges.json"], stdout=subprocess.DEVNULL, shell=True)
        print("[+] Tools directory successfully created")
    print("[-] Pulling IP Ranges from JSON...")
    f = open(f'{home_dir}/Wordlists/aws-ip-ranges.json')
    aws_ips = json.load(f)
    ip_ranges = []
    ip_ranges_str = ""
    for ip_range in aws_ips['prefixes']:
        ip_ranges.append(ip_range['ip_prefix'])
        ip_ranges_str += f"{ip_range['ip_prefix']}\n"
    f.close()
    f = open("/tmp/aws_ips.tmp", "w")
    f.write(ip_ranges_str)
    f.close()

    print(f"[-] Running initial scan to identify hosts...")
    ip_count = subprocess.run([f"nmap -n -sL -iL /tmp/aws_ips.tmp | wc -l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    ips = ip_count.stdout.replace("\n", "")

    print(f"[-] Running masscan against {ips} IPs...")
    subprocess.run([f"sudo {home_dir}/Tools/masscan/bin/masscan -p443 --rate 40000 -iL /tmp/aws_ips.tmp -oL /tmp/clear_sky_masscan.tmp"], shell=True)
    subprocess.run(["cat /tmp/clear_sky_masscan.tmp | awk {'print $4'} | awk NF | sort -u > /tmp/tls-scan-in.tmp"], shell=True)
    
    print(f"[+] Successfully completed running masscan against {ips} IPs!")

    print(f"[-] Running tls-scan on masscan results to collect SSL/TLS Certificates...")
    subprocess.run([f"cat /tmp/tls-scan-in.tmp | {home_dir}/Tools/tls-scan/tls-scan --port=443 --concurrency=150 --cacert={home_dir}/Tools/tls-scan/ca-bundle.crt 2>/dev/null -o /tmp/tls-results.json"], shell=True)
    print(f"[+] Successfully completed the tls-scan!")

print(f"[-] Using jq to parse for the FQDN...")
subprocess.run([f"""cat /tmp/tls-results.json | jq --slurp -r '.[]? | select(.certificateChain[]?.subject | test("{fqdn}")) | .ip | @text' > /tmp/tls_filtered.tmp"""], shell=True)
print(f"[+] Successfully parsed tls-scan results!")
now = datetime.now().strftime("%d-%m-%y_%I%p")
results_str = subprocess.run([f"cat /tmp/tls_filtered.tmp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
results_arr = results_str.stdout.split("\n")
directory_check = subprocess.run([f"ls {home_dir}/Reports"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
if directory_check.returncode == 0:
    print("[+] Identified Reports directory")
else:
    print("[!] Could not locate Reports directory -- Creating now...")
    cloning = subprocess.run([f"mkdir ~/Reports"], stdout=subprocess.DEVNULL, shell=True)
    print("[+] Reports directory successfully created")
print(f"[-] Running final NMap scan on identified targets...")
subprocess.run([f"rm -rf {home_dir}/Reports/ClearSky_{fqdn}_*"], shell=True)
if len(results_arr) < 10:
    subprocess.run([f"nmap -T 4 -iL /tmp/tls_filtered.tmp -Pn --script=http-title -p- --open > {home_dir}/Reports/ClearSky_{fqdn}_{now}"], shell=True)
else:
    subprocess.run([f"nmap -T 4 -iL /tmp/tls_filtered.tmp -Pn --script=http-title --top-ports 100 --open > {home_dir}/Reports/ClearSky_{fqdn}_{now}"], shell=True)
print(f"[+] NMap scan completed successfully!  A report has been created in the ~/Reports directory")

print(f"[-] Updating database...")
r = requests.post(f'http://{server_ip}:{server_port}/api/auto', data={'fqdn':fqdn})
thisFqdn = r.json()
thisFqdn['recon']['subdomains']['cloudRanges'] = results_arr
final_request = requests.post(f'http://{server_ip}:{server_port}/api/auto/update', json=thisFqdn, headers={'Content-type':'application/json'})
if final_request.status_code == 200:
    print("[+] Clear_sky.py completed successfully!")
else:
    print("[!] Clear_sky.py did NOT complete successfully!")