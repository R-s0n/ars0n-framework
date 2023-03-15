import requests
import subprocess
import argparse
import json
from datetime import datetime, timedelta

class Timer:
    def __init__(self):
        self.start = datetime.now()
        self.stop = None
    
    def stop_timer(self):
        self.stop = datetime.now()

    def get_start(self):
        return self.start.strftime("%H:%M:%S")

    def get_stop(self):
        return self.stop.strftime("%H:%M:%S")

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def get_fqdn_obj(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    return r.json()

def get_fqdn_vulns(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    thisFqdn = r.json()
    return thisFqdn['data']

def clear_vulns(args):
    thisFqdn = get_fqdn_obj(args)
    thisFqdn['vulns'] = json.loads("{}")
    update_fqdn_obj(args, thisFqdn)

def update_vulns(args, thisFqdn, data):
    res = requests.post(f"http://{args.server}:{args.port}/api/auto", data={"fqdn":args.fqdn})
    thisFqdn = res.json()
    for vuln in data:
        thisFqdn['vulns'].append(vuln)
    build_slack_message(args, thisFqdn, data)
    requests.post(f'http://{args.server}:{args.port}/api/auto/update', json=thisFqdn)

def update_fqdn_obj(args, thisFqdn):
    requests.post(f'http://{args.server}:{args.port}/api/auto/update', json=thisFqdn)

def update_nuclei():
    home_dir = get_home_dir()
    print("[-] Updating Nuclei and Nuclei Templates...")
    subprocess.run([f'export PATH="$HOME/go/bin:$PATH"; {home_dir}/go/bin/nuclei -update -ut;'], shell=True)

def build_url_str(thisFqdn):
    httprobe_arr = thisFqdn['recon']['subdomains']['httprobe']
    masscan_arr = thisFqdn['recon']['subdomains']['masscanLive']
    urls = httprobe_arr + masscan_arr
    url_str = ""
    for url in urls:
        url_str += f"{url}\n"
    return url_str

def write_urls_file(url_str):
    f = open("/tmp/urls.txt", "w")
    f.write(url_str)
    f.close()

def full_nuclei_scan(args, now):
    home_dir = get_home_dir()
    subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates -l /tmp/urls.txt -stats -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
    data = process_results(args, now)
    thisFqdn = get_fqdn_obj(args)
    update_vulns(args, thisFqdn, data)

def misconfiguration_nuclei_scan(args, now):
    home_dir = get_home_dir()
    subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/misconfiguration -l /tmp/urls.txt -stats -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
    data = process_results(args, now)
    thisFqdn = get_fqdn_obj(args)
    update_vulns(args, thisFqdn, data)

def cves_nuclei_scan(args, now):
    home_dir = get_home_dir()
    subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/cves -l /tmp/urls.txt -stats -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
    data = process_results(args, now)
    thisFqdn = get_fqdn_obj(args)
    update_vulns(args, thisFqdn, data)

def cnvd_nuclei_scan(args, now):
    home_dir = get_home_dir()
    subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/cnvd -l /tmp/urls.txt -stats -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
    data = process_results(args, now)
    thisFqdn = get_fqdn_obj(args)
    update_vulns(args, thisFqdn, data)

def exposed_panels_nuclei_scan(args, now):
    home_dir = get_home_dir()
    subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/exposed-panels -l /tmp/urls.txt -stats -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
    data = process_results(args, now)
    thisFqdn = get_fqdn_obj(args)
    update_vulns(args, thisFqdn, data)

def miscellaneous_nuclei_scan(args, now):
    home_dir = get_home_dir()
    subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/miscellaneous -l /tmp/urls.txt -stats -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
    data = process_results(args, now)
    thisFqdn = get_fqdn_obj(args)
    update_vulns(args, thisFqdn, data)

def network_nuclei_scan(args, now):
    home_dir = get_home_dir()
    subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/network -l /tmp/urls.txt -stats -fhr -hmY -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
    data = process_results(args, now)
    thisFqdn = get_fqdn_obj(args)
    update_vulns(args, thisFqdn, data)

def process_results(args, now):
    f = open(f"/tmp/{args.fqdn}-{now}.json")
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
    return data

def build_slack_message(args, thisFqdn, data):
    info_counter = 0
    non_info_counter = 0
    for result in data:
        if result['info']['severity'] == 'info':
            info_counter += 1
            result['impactful'] = False
        else :
            non_info_counter += 1
            result['impactful'] = True
    message_json = {'text':f'Nuclei Scan Completed!\n\nResults:\nWeb Servers Scanned: {target_count}\nRood/Seed Targeted: {args.fqdn}\nTemplate Category: {args.template}\nImpactful Results: {non_info_counter}\nInformational Results: {info_counter}\n\nNothing wrong with a little Spray and Pray!!  :pray:','username':'Vuln Disco Box','icon_emoji':':dart:'}
    f = open(f'{home_dir}/.keys/slack_web_hook')
    token = f.read()
    f.close()
    requests.post(f'https://hooks.slack.com/services/{token}', json=message_json)     

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=True)
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=True)
    parser.add_argument('-d','--fqdn', help='Name of the Root/Seed FQDN', required=True)
    parser.add_argument('-f','--full', help='Name of the Root/Seed FQDN', required=False, action='store_true')
    return parser.parse_args()
    
def main(args):
    starter_timer = Timer()
    clear_vulns(args)
    update_nuclei()
    thisFqdn = get_fqdn_obj(args)
    url_str = build_url_str(thisFqdn)
    write_urls_file(url_str)
    now = str(datetime.now()).split(" ")[0]
    if args.full:
        full_nuclei_scan(args, now)
    else:
        misconfiguration_nuclei_scan(args, now)
        cves_nuclei_scan(args, now)
        cnvd_nuclei_scan(args, now)
        exposed_panels_nuclei_scan(args, now)
        miscellaneous_nuclei_scan(args, now)
        network_nuclei_scan(args, now)
    starter_timer.stop_timer()
    print(f"[+] Fire Starter Modules Done!  Start: {starter_timer.get_start()}  |  Stop: {starter_timer.get_stop()}")

if __name__ == "__main__":
    args = arg_parse()
    main(args)