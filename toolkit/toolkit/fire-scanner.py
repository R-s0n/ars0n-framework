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
    thisFqdn['vulnsSSL'] = json.loads("{}")
    thisFqdn['vulnsFile'] = json.loads("{}")
    thisFqdn['vulnsDNS'] = json.loads("{}")
    thisFqdn['vulnsVulns'] = json.loads("{}")
    thisFqdn['vulnsTech'] = json.loads("{}")
    thisFqdn['vulnsMisconfig'] = json.loads("{}")
    thisFqdn['vulnsCVEs'] = json.loads("{}")
    thisFqdn['vulnsCNVD'] = json.loads("{}")
    thisFqdn['vulnsExposed'] = json.loads("{}")
    thisFqdn['vulnsExposure'] = json.loads("{}")
    thisFqdn['vulnsMisc'] = json.loads("{}")
    thisFqdn['vulnsNetwork'] = json.loads("{}")
    thisFqdn['vulnsRs0n'] = json.loads("{}")
    thisFqdn['vulnsHeadless'] = json.loads("{}")
    update_fqdn_obj(args, thisFqdn)

def update_vulns(args, thisFqdn, data, template, key):
    res = requests.post(f"http://{args.server}:{args.port}/api/auto", data={"fqdn":args.fqdn})
    thisFqdn = res.json()
    for vuln in data:
        thisFqdn[key].append(vuln)
    build_slack_message(args, thisFqdn, data, template)
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
    try:
        print("[-] Running a Full Nuclei Scan using All Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "All Templates", "vulns")
    except Exception as e:
        print("[!] Something went wrong!  Exiting...")

def misconfiguration_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the Misconfiguration Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/misconfiguration -l /tmp/urls.txt -timeout 7 -validate -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Misconfigurations", "vulnsMisc")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the Misconfiguration Templates...")


def cves_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the CVEs Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/cves -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "CVES", "vulnsCVEs")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the CVEs Templates...")

def cnvd_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the CNVD Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/cnvd -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "CNVD", "vulnsCNVD")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the CNVD Templates...")

def exposed_panels_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the Exposed Panels Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/exposed-panels -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Exposed Panels", "vulnsExposed")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the Exposed Panels Templates...")

def exposures_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the Exposures Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/exposures -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Exposures", "vulnsExposure")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the Exposures Templates...")

def miscellaneous_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the Miscellaneous Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/miscellaneous -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Miscellaneous", "vulnsMisc")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the Miscellaneous Templates...")

def network_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the Network Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/network -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Network", "vulnsNetwork")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the Network Templates...")

def file_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the File Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/file -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "File", "vulnsFile")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the File Templates...")

def dns_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the DNS Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/dns -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "DNS", "vulnsDNS")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the DNS Templates...")

def vulnerabilities_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the Vulnerabilities Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/vulnerabilities -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Vulnerabilities", "vulnsVulns")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the Vulnerabilities Templates...")

def technologies_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the Technologies Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/technologies -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Technologies", "vulnsTech")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the Technologies Templates...")

def rs0n_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the Custom Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t ./custom -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -vv --headless -hbs 10 -headc 1 -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Custom", "vulnsRs0n")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the Custom Templates...")

def headless_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the Headless Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/headless -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -vv --headless -hbs 10 -headc 1 -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Headless", "vulnsHeadless")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the Headless Templates...")

def ssl_nuclei_scan(args, now):
    try:
        print("[-] Running a Nuclei Scan using the SSL Templates")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/ssl -l /tmp/urls.txt -stats -config config/nuclei_config.yaml -fhr -hm -o /tmp/{args.fqdn}-{now}.json -json"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "SSL", "vulnsSSL")
    except Exception as e:
        print("[!] Something went wrong!  Skipping the SSL Templates...")

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

def build_slack_message(args, thisFqdn, data, template):
    info_counter = 0
    non_info_counter = 0
    for result in data:
        if len(result['info']['name']) < 2:
            data.remove(result)
            continue
        if result['info']['severity'] == 'info':
            info_counter += 1
            result['impactful'] = False
        else :
            non_info_counter += 1
            result['impactful'] = True
    httprobe_arr = thisFqdn['recon']['subdomains']['httprobe']
    masscan_arr = thisFqdn['recon']['subdomains']['masscanLive']
    urls = httprobe_arr + masscan_arr
    target_count = len(urls)
    if non_info_counter != 0 or info_counter != 0:
        message_json = {'text':f'Nuclei Scan Completed!\n\nResults:\nWeb Servers Scanned: {target_count}\nRood/Seed Targeted: {args.fqdn}\nTemplate Category: {template}\nImpactful Results: {non_info_counter}\nInformational Results: {info_counter}\n\nNothing wrong with a little Spray and Pray!!  :pray:','username':'Vuln Disco Box','icon_emoji':':dart:'}
        home_dir = get_home_dir()
        f = open(f'{home_dir}/.keys/slack_web_hook')
        token = f.read()
        f.close()
        slack_auto = requests.post(f'https://hooks.slack.com/services/{token}', json=message_json) 
        print(f"[+] Slack Notification Sent!  {non_info_counter} Impactful Findings!")

def clean_screenshots():
    subprocess.run("mv -f http*.png ./screenshots/", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def clean_stacktrace_dumps():
    subprocess.run("mv -f nuclei-*.dump ./logs/", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=True)
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=True)
    parser.add_argument('-d','--fqdn', help='Name of the Root/Seed FQDN', required=True)
    parser.add_argument('-f','--full', help='Name of the Root/Seed FQDN', required=False, action='store_true')
    return parser.parse_args()
    
def main(args):
    starter_timer = Timer()
    clean_screenshots()
    clean_stacktrace_dumps()
    clear_vulns(args)
    update_nuclei()
    thisFqdn = get_fqdn_obj(args)
    url_str = build_url_str(thisFqdn)
    write_urls_file(url_str)
    now = str(datetime.now()).split(" ")[0]
    if args.full:
        full_nuclei_scan(args, now)
    else:
        ssl_nuclei_scan(args, now)
        file_nuclei_scan(args, now)
        dns_nuclei_scan(args, now)
        vulnerabilities_nuclei_scan(args, now)
        technologies_nuclei_scan(args, now)
        misconfiguration_nuclei_scan(args, now)
        cves_nuclei_scan(args, now)
        cnvd_nuclei_scan(args, now)
        exposed_panels_nuclei_scan(args, now)
        exposures_nuclei_scan(args, now)
        miscellaneous_nuclei_scan(args, now)
        # network_nuclei_scan(args, now)
        rs0n_nuclei_scan(args, now)
        headless_nuclei_scan(args, now)
    starter_timer.stop_timer()
    print(f"[+] Fire Starter Modules Done!  Start: {starter_timer.get_start()}  |  Stop: {starter_timer.get_stop()}")

if __name__ == "__main__":
    args = arg_parse()
    main(args)