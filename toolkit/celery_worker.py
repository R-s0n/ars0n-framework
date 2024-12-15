from celery import Celery
import subprocess
import requests
import re
import json

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379"
)

def parse_amass_file(file_path):
    try:
        asns = []
        cidr_subnets = []
        isps = []
        ipv4_addresses = []
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if "contains" in line:
                    cidr_subnets.append(line.split("\n")[0])
                if "announces" in line:
                    asns.append(line.split("\n")[0])
                if "managed_by" in line:
                    isps.append(line.split("\n")[0])
                ipv4_match = re.match(r'\d+\.\d+\.\d+\.\d+', line)
                if ipv4_match:
                    ipv4_addresses.append(ipv4_match.group())
        return {
            "asns": asns,
            "cidr_subnets": cidr_subnets,
            "isps": isps,
            "ipv4_addresses": ipv4_addresses
        }
    except Exception as e:
        print("[!] Unable to pull IPs and/or ASNs...")
        print(f"[!] Exception: {e}")

def get_ips_from_amass(thisFqdn):
    result = parse_amass_file("./temp/amass.tmp")
    thisFqdn['asns'] = result["asns"]
    thisFqdn['subnets'] = result["cidr_subnets"]
    thisFqdn['isps'] = result["isps"]
    for ip_address in result["ipv4_addresses"]:
        exists = False
        for ip_obj in thisFqdn['ips']:
            if ip_address == ip_obj['ip']:
                exists = True
        if exists == False:
            data = {
                "ip": ip_address,
                "ports": []
            }
            loaded_data = json.dumps(data)
            thisFqdn['ips'].append(json.loads(loaded_data))
    return thisFqdn

def amass_get_dns():
    amass_file = open(f"./temp/amass.tmp", 'r')
    amass_file_lines = amass_file.readlines()
    amass_file.close()
    dns = {
        "arecord": [],
        "aaaarecord": [],
        "cnamerecord": [],
        "mxrecord": [],
        "txtrecord": [],
        "node": [],
        "nsrecord": [],
        "srvrecord": [],
        "ptrrecord": [],
        "spfrecord": [],
        "soarecord": []
    }
    for line in amass_file_lines:
        if "a_record" in line and "aaaa_record" not in line:
            dns['arecord'].append(line.split("\n")[0])
        if "aaaa_record" in line:
            dns['aaaarecord'].append(line.split("\n")[0])
        if "cname_record" in line:
            dns['cnamerecord'].append(line.split("\n")[0])
        if "mx_record" in line:
            dns['mxrecord'].append(line.split("\n")[0])
        if "txt_record" in line:
            dns['txtrecord'].append(line.split("\n")[0])
        if "node" in line:
            dns['node'].append(line.split("\n")[0])
        if "ns_record" in line:
            dns['nsrecord'].append(line.split("\n")[0])
        if "srv_record" in line:
            dns['srvrecord'].append(line.split("\n")[0])
        if "ptr_record" in line:
            dns['ptrrecord'].append(line.split("\n")[0])
        if "spf_record" in line:
            dns['spfrecord'].append(line.split("\n")[0])
        if "soa_record" in line:
            dns['soarecord'].append(line.split("\n")[0])
    return dns

@celery_app.task
def test_amass(domain):
    try:
        print(f"Running Amass Against {domain}...")
        print(f"Domain: {domain}")
        r = requests.post(f'http://backend:8000/api/auto', data={'fqdn':domain})
        initFqdn = r.json()
        amass_results = subprocess.run([f"amass enum -active -alts -brute -nocolor -min-for-recursive 2 -timeout 60 -d {domain} -o ./temp/amass.tmp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        print(f"STDOUT: {amass_results.stdout}")
        print(f"STDERR: {amass_results.stderr}")
        amass_arr = []
        with open('./temp/amass.tmp', 'r') as file:
            for line in file:
                try:
                    domain_pattern = r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
                    match = re.search(domain_pattern, line)
                    if match:
                        domain = match.group(1)
                        amass_arr.append(domain)
                except Exception as e:
                    print(f"[!] Error processing line: {line}")
                    print(f"[!] Exception: {e}")
        thisFqdn = get_ips_from_amass(initFqdn)
        print("thisFqdn:")
        print(thisFqdn)
        thisFqdn['dns'] = amass_get_dns()
        final_amass_arr = []
        for amass_finding in amass_arr:
            if thisFqdn['fqdn'] in amass_finding and amass_finding not in final_amass_arr:
                final_amass_arr.append(amass_finding)
        thisFqdn['recon']['subdomains']['amass'] = final_amass_arr
        print("final update")
        print(thisFqdn)
        r = requests.post(f'http://backend:8000/api/auto/update', json=thisFqdn)
        try:
            print(r.text)
        except:
            print("it's not r.text")
        return "Amass Scan Complete"
    except Exception as e:
        print("SOMETHING'S WRONG WITH THE AMASS SCAN")
        return "SOMETHING'S WRONG WITH THE AMASS SCAN"