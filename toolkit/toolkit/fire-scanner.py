import requests
import subprocess
import argparse
import json
import re
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
    
class Logger:
    def __init__(self):
        subprocess.run(["[ -f logs/log.txt ] || touch logs/log.txt"], shell=True)
        with open("logs/log.txt", "r") as file:
            self.init_log_data = file.readlines()
            self.init_log_len = len(self.init_log_data)
        with open("logs/log.txt", "a") as file:
            log_start_time = datetime.now()
            flag = "[INIT]"
            running_script = "Fire-Scanner.py"
            message = "Logger Initialized"
            file.write(f"{flag} {log_start_time} | {running_script} -- {message}\n")

    def write_to_log(self, flag, running_script, message):
        with open("logs/log.txt", "a") as file:
            log_start_time = datetime.now()
            file.write(f"{flag} {log_start_time} | {running_script} -- {message}\n")
        with open("logs/temp_log.txt", "a") as file:
            log_start_time = str(datetime.now())
            file.write(f"{flag} {log_start_time} | {running_script} -- {message}\n")

class NetworkValidator:
    def __init__(self):
        self.process_id = None
        self.interface_data = None
        self.tunnel_ip = None
        self.gateway_ip = None
        self.vpn_on = self.check_vpn()
        self.resolver_string = self.get_resolver_string()
        self.vpn_connected = self.check_vpn_connection()

    def __repr__(self):
        return f"\n** Network Validator **\n\nProtonVPN Running: {self.vpn_on}\nProtonVPN Process ID: {self.process_id}\nProtonVPN Tunnel IP: {self.tunnel_ip}\nProtonVPN Gateway IP: {self.gateway_ip}\nInterface Data:\n{self.interface_data}\nResolvers File:\n{self.resolver_string}\n"
    
    def check_vpn(self):
        print("[-] Checking for ProtonVPN Process ID...")
        vpn_check = subprocess.run(["pgrep protonvpn"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
        if vpn_check.returncode == 0:
            final_process_id = vpn_check.stdout.replace("\n", "")
            print(f"[+] ProtonVPN found on Process ID {final_process_id}")
            self.process_id = final_process_id
            return True
        else:
            print("[-] ProtonVPN Process ID not found.  If you are running ProtonVPN, something has gone wrong.  Otherwise, ignore this message :)")
            return False

    def get_resolver_string(self):
        print("[-] Storing contents of the /etc/resolv.con file...")
        resolver_string = subprocess.run(["cat /etc/resolv.conf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if resolver_string.returncode == 0:
            final_string = resolver_string.stdout
            print("[+] Contents of /etc/resolv.conf stored successfully!")
            return final_string
        else:
            print("[!] Unable to store contents of /etc/resolv.conf file!  If anything breaks, you're on your own...")
            return ""

    def check_vpn_connection(self):
        print("[-] Checking VPN Connection...")
        validation_count = 0
        interface_check = subprocess.run(["ifconfig | grep -A 1 proton"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if interface_check.returncode == 0:
            validation_count += 1
            print("[+] ProtonVPN Connection Found!  Storing relavent data...")
            interface_check_stdout = interface_check.stdout
            self.interface_data = interface_check_stdout
            pattern = r'inet\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            match = re.search(pattern, interface_check_stdout)
            if match:
                validation_count += 1
                inet_ip = match.group(1)
                print(f"[+] ProtonVPN Tunnel IP: {inet_ip}")
                self.tunnel_ip = inet_ip
            pattern = r'destination\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            match = re.search(pattern, interface_check_stdout)
            if match:
                validation_count += 1
                found_gateway_ip = match.group(1)
                print(f"[+] ProtonVPN Gateway IP: {found_gateway_ip}")
                self.gateway_ip = found_gateway_ip
        if validation_count == 3:
            print("[+] ProtonVPN Connection Confirmed!")
            self.vpn_connected = True
        else:
            print("[+] ProtonVPN connection not found.  Continuing without VPN...")
            self.vpn_connected = False

def protonvpn_connect():
    command = subprocess.run(["protonvpn-cli c -f"], stdout=subprocess.PIPE, text=True, shell=True)

def protonvpn_disconnect():
    command = subprocess.run(["protonvpn-cli d"], stdout=subprocess.PIPE, text=True, shell=True)

def protonvpn_status():
    command = subprocess.run(["protonvpn-cli s"], stdout=subprocess.PIPE, text=True, shell=True)
    return command.stdout
    
def protonvpn_killswitch_on():
    command = subprocess.run(["protonvpn-cli ks --on"], shell=True)

def protonvpn_killswitch_off():
    command = subprocess.run(["protonvpn-cli ks --off"], shell=True)

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def validate_network_connection(logger):
        print("[-] Checking Network Connection...")
        try:
            subprocess.run(["curl https://google.com"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        except Exception as e:
            logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Network Connectivity Lost!  Exiting...")
            exit()

def get_fqdn_obj(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    return r.json()

def get_fqdn_vulns(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    thisFqdn = r.json()
    return thisFqdn['data']

def clear_vulns(args):
    thisFqdn = get_fqdn_obj(args)
    thisFqdn['vulns'] = json.loads("[]")
    thisFqdn['vulnsSSL'] = json.loads("[]")
    thisFqdn['vulnsFile'] = json.loads("[]")
    thisFqdn['vulnsDNS'] = json.loads("[]")
    thisFqdn['vulnsVulns'] = json.loads("[]")
    thisFqdn['vulnsTech'] = json.loads("[]")
    thisFqdn['vulnsMisconfig'] = json.loads("[]")
    thisFqdn['vulnsCVEs'] = json.loads("[]")
    thisFqdn['vulnsCNVD'] = json.loads("[]")
    thisFqdn['vulnsExposed'] = json.loads("[]")
    thisFqdn['vulnsExposure'] = json.loads("[]")
    thisFqdn['vulnsMisc'] = json.loads("[]")
    thisFqdn['vulnsNetwork'] = json.loads("[]")
    thisFqdn['vulnsRs0n'] = json.loads("[]")
    thisFqdn['vulnsHeadless'] = json.loads("[]")
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

def update_nuclei(logger):
    home_dir = get_home_dir()
    print("[-] Updating Nuclei and Nuclei Templates...")
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Updating Nuclei...")
    try:
        subprocess.run([f'export PATH="$HOME/go/bin:$PATH"; {home_dir}/go/bin/nuclei -update -ut;'], shell=True)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuclei Update Succesful!")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Nuclei Update Was NOT Successful!  Exception: {e}")

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
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "All Templates", "vulns")
    except Exception as e:
        print("[!] Something went wrong!  Exiting...")

def protonvpn_unnecessary(args, template_name):
    if args.proton and "No active Proton VPN connection." not in protonvpn_status():
            print(f"[!] ProtonVPN is NOT needed for the {template_name} scan.  Disconnecting the VPN...")
            protonvpn_disconnect()

def protonvpn_necessary(args, template_name):
    if args.proton and "No active Proton VPN connection." in protonvpn_status():
            print(f"[!] ProtonVPN is needed for the {template_name} scan.  Disconnecting the VPN...")
            protonvpn_connect()

def technologies_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (Technologies) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the Technologies Templates")
        protonvpn_unnecessary(args, "Technologies")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/technologies -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Technologies", "vulnsTech")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (Technologies) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (Technologies) Failed!  Exception: {e}")
        print(f"[!] Exception: {e}")


def misconfiguration_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (Misconfiguration) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the Misconfiguration Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/misconfiguration -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -timeout 7 -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Misconfigurations", "vulnsMisconfig")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (Misconfiguration) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (Misconfiguration) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the Misconfiguration Templates...")


def cves_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (CVEs) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the CVEs Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/cves -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -timeout 7 -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "CVES", "vulnsCVEs")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (CVEs) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (CVEs) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the CVEs Templates...")

def cnvd_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (CNVD) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the CNVD Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/cnvd -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "CNVD", "vulnsCNVD")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (CNVD) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (CNVD) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the CNVD Templates...")

def exposed_panels_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (Exposed Panels) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the Exposed Panels Templates")
        protonvpn_necessary(args, "Exposed Panels")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/exposed-panels -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Exposed Panels", "vulnsExposed")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (Exposed Panels) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (Exposed Panels) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the Exposed Panels Templates...")

def exposures_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (Exposures) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the Exposures Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/exposures -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Exposures", "vulnsExposure")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (Exposures) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (Exposures) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the Exposures Templates...")

def miscellaneous_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (Miscellaneous) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the Miscellaneous Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/miscellaneous -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Miscellaneous", "vulnsMisc")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (Miscellaneous) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (Miscellaneous) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the Miscellaneous Templates...")

def network_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (Network) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the OSINT Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/osint -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Network", "vulnsNetwork")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (Network) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (Network) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the Network Templates...")

def file_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (File) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the File Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/default-logins -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "File", "vulnsFile")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (File) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (File) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the File Templates...")

def dns_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (DNS) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the DNS Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/dns -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "DNS", "vulnsDNS")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (DNS) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (DNS) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the DNS Templates...")

def vulnerabilities_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (Vulnerabilities) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the Vulnerabilities Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/http/vulnerabilities -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -timeout 7 -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Vulnerabilities", "vulnsVulns")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (Vulnerabilities) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (Vulnerabilities) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the Vulnerabilities Templates...")


def rs0n_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (rs0n) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the Custom Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t ./custom -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats --headless -sb -hbs 10 -headc 1 -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Custom", "vulnsRs0n")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (rs0n) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (rs0n) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the Custom Templates...")

def headless_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (Headless) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the Headless Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/headless -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats --headless -sb -hbs 10 -headc 1 -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "Headless", "vulnsHeadless")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (Headless) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (Headless) Failed!  Exception: {e}")
        print("[!] Something went wrong!  Skipping the Headless Templates...")

def ssl_nuclei_scan(args, now, logger):
    logger.write_to_log("[MSG]","Fire-Scanner.py",f"Running Nuclei (SSL) -> {args.fqdn}")
    try:
        print("[-] Running a Nuclei Scan using the SSL Templates")
        protonvpn_necessary(args, "Misconfigurations")
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/ssl -l /tmp/urls.txt -timeout 3 -irt 1m30s -mhe 15 -ldp -stats -fr -hm -o /tmp/{args.fqdn}-{now}.json -jsonl"], shell=True)
        data = process_results(args, now)
        thisFqdn = get_fqdn_obj(args)
        update_vulns(args, thisFqdn, data, "SSL", "vulnsSSL")
        if args.proton:
            protonvpn_disconnect()
        validate_network_connection(logger)
        results_count = len(data)
        logger.write_to_log("[MSG]","Fire-Scanner.py",f"Nuceli Scan (SSL) Completed Successfully w/ {results_count} Results Against {thisFqdn['fqdn']}")
    except Exception as e:
        if args.proton:
            protonvpn_disconnect()
        logger.write_to_log("[ERROR]","Fire-Scanner.py",f"Running Nuclei (SSL) Failed!  Exception: {e}")
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
    subprocess.run("rm -f nuclei-*.dump", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run("rm -f crash-*.dump", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def move_screenshots():
    subprocess.run("""for file in ./screenshots/*; do cp -f "$file" "../client/public/screenshots/$(basename "$file")"; done""", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def perform_scans(args, thisFqdn, now, logger):
    """
    Perform various scanning routines based on the provided arguments.

    :param args: Command line arguments passed to the script.
    :param thisFqdn: FQDN object containing domain information.
    :param now: Current datetime as a string.
    :param logger: Logger object for logging.
    """
    url_str = build_url_str(thisFqdn)
    write_urls_file(url_str)

    if args.full:
        full_nuclei_scan(args, now)
    else:
        # List of scan functions to run
        scan_functions = [
            technologies_nuclei_scan,
            exposed_panels_nuclei_scan,
            misconfiguration_nuclei_scan,
            exposures_nuclei_scan,
            rs0n_nuclei_scan,
            headless_nuclei_scan,
            dns_nuclei_scan,
            ssl_nuclei_scan,
            vulnerabilities_nuclei_scan,
            cves_nuclei_scan,
            # You can include or exclude other scans as needed
            # file_nuclei_scan,
            # network_nuclei_scan,
            # cnvd_nuclei_scan,
            # miscellaneous_nuclei_scan,
        ]

        # Execute each scan function
        for scan_function in scan_functions:
            scan_function(args, now, logger)

def update_scan_progress(scan_step_name, target_domain):
    requests.post("http://localhost:5000/update-scan", json={"stepName":scan_step_name,"target_domain":target_domain})

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=True)
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=True)
    parser.add_argument('-d','--fqdn', help='Name of the Root/Seed FQDN', required=True)
    parser.add_argument('-f','--full', help='Name of the Root/Seed FQDN', required=False, action='store_true')
    parser.add_argument('-p','--proton', help='Run all scans through ProtonVPN', required=False, action='store_true')
    # parser.add_argument('--single', help='Run scan for a single domain', required=True)
    return parser.parse_args()

def main(args):
    starter_timer = Timer()
    # network_validator = NetworkValidator()
    logger = Logger()
    clean_screenshots()
    clean_stacktrace_dumps()
    clear_vulns(args)
    update_nuclei(logger)
    thisFqdn = get_fqdn_obj(args)
    url_str = build_url_str(thisFqdn)
    write_urls_file(url_str)
    now = str(datetime.now()).split(" ")[0]
    if args.full:
        full_nuclei_scan(args, now)
    else:
        ## Safe Templates
        update_scan_progress("Fire-Scanner | Technologies", args.fqdn)
        technologies_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | Exposed Panels", args.fqdn)
        exposed_panels_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | Misconfiguration", args.fqdn)
        misconfiguration_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | Exposures", args.fqdn)
        exposures_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | rs0n", args.fqdn)
        rs0n_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | Headless", args.fqdn)
        headless_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | DNS", args.fqdn)
        dns_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | SSL", args.fqdn)
        ssl_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | Vulnerabilities", args.fqdn)
        vulnerabilities_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | CVE's", args.fqdn)
        cves_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | File", args.fqdn)
        file_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | CNVD", args.fqdn)
        cnvd_nuclei_scan(args, now, logger)
        update_scan_progress("Fire-Scanner | Misc", args.fqdn)
        miscellaneous_nuclei_scan(args, now, logger)
        ## Unsafe Templates
        # network_nuclei_scan(args, now, logger)
    move_screenshots()   
    starter_timer.stop_timer()
    # protonvpn_killswitch_off()
    logger.write_to_log("[DONE]","Fire-Scanner.py",f"Fire-Scanner Completed Successfully -> {args.fqdn}")
    print(f"[+] Fire Starter Modules Done!  Start: {starter_timer.get_start()}  |  Stop: {starter_timer.get_stop()}")

if __name__ == "__main__":
    args = arg_parse()
    main(args)