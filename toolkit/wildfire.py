import requests, argparse, subprocess, json, os
from time import sleep
from datetime import datetime

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
        subprocess.run(["[ -f logs/log.txt ] || touch logs/log.txt; rm -f logs/temp_log.txt"], shell=True)
        with open("logs/log.txt", "r") as file:
            self.init_log_data = file.readlines()
            self.init_log_len = len(self.init_log_data)
        with open("logs/log.txt", "a") as file:
            log_start_time = datetime.now()
            flag = "[INIT]"
            running_script = "Wildfire.py"
            message = "Logger Initialized"
            file.write(f"{flag} {log_start_time} | {running_script} -- {message}\n")

    def write_to_log(self, flag, running_script, message):
        with open("logs/log.txt", "a") as file:
            log_start_time = str(datetime.now())
            file.write(f"{flag} {log_start_time} | {running_script} -- {message}\n")
        with open("logs/temp_log.txt", "a") as file:
            log_start_time = str(datetime.now())
            file.write(f"{flag} {log_start_time} | {running_script} -- {message}\n")

    def create_datebase_log(self, args):
        try:
            subprocess.run(["[ -f logs/log.txt ] || touch logs/log.txt"], shell=True)
            logEntry = {
                "scan":"Wildfire.py -- " + str(datetime.now()),
                "logFile":[]
            }
            with open("logs/temp_log.txt", "r") as file:
                    clean_log_file = []
                    for line in file.readlines():
                        if len(line.strip()) > 3:
                            clean_log_file.append(line.strip())
                    logEntry['logFile'] = clean_log_file
            print(logEntry)
            res = requests.post(f"http://{args.server}:{args.port}/api/log/new", json=logEntry)
            print(res.json())
            # subprocess.run(['''curl -X POST http://localhost:8000/api/log/new -d '{"scan":"Wildfire.py -- ''' + str(datetime.now()) + '''","logFile":''' + str(file.readlines()) + '''}' -H "Content-Type: application/json"; rm logs/temp_log.txt'''], shell=True)
        except Exception as e:
            self.write_to_log("[ERROR]","Wildfire.py",f"Error Updating Log Database! Exception: {str(e)}")
            print("[!] Error Adding Logs to Datebase!  Skipping...")

def get_fqdns(args):
    res = requests.post(f"http://{args.server}:{args.port}/api/fqdn/all")
    return res

def clean_screenshots(args):
    res = get_fqdns(args)
    fqdns = json.loads(res.text)
    screenshots = os.listdir("../client/public/screenshots")
    for screenshot in screenshots:
        if ".gitkeep" in screenshot:
            continue
        delete_screenshot = True
        print(f"[-] Checking Screenshot: {screenshot}")
        for fqdn in fqdns:
            if fqdn['fqdn'] in screenshot:
                print(f"[+] Screenshot {screenshot} should NOT be deleted.")
                delete_screenshot = False
        if delete_screenshot:
            subprocess.run([f"rm -f ../client/public/screenshots/{screenshot}"], shell=True)


def sort_fqdns(fqdns):
    sorted_fqdns = []
    while len(fqdns) > 0:
        last_updated = fqdns[0]
        for fqdn in fqdns:
            if last_updated['updatedAt'] > fqdn['updatedAt']:
                last_updated = fqdn
        fqdns.remove(last_updated)
        sorted_fqdns.append(last_updated)
    return sorted_fqdns

def start_single_domain(args, logger, fqdn):
    if fqdn not in args.blacklist:
        print(f"[-] Running Fire-Starter Modules (Subdomain Recon) against targeted domain: {fqdn}")
        logger.write_to_log("[MSG]", "Wildfire.py", f"Running Fire-Starter.py -> {fqdn}")
        try:
            subprocess.run([f'python3 toolkit/fire-starter.py -d {fqdn} -S {args.server} -P {args.port} -p {args.proxy}'], shell=True)
        except Exception as e:
            print(f"[!] Exception: {e}")

def cloud_single_domain(args, logger, fqdn):
    if fqdn not in args.blacklist:
        print(f"[-] Running Fire-Cloud Modules against targeted domain: {fqdn}")
        logger.write_to_log("[MSG]", "Wildfire.py", f"Running Fire-Cloud.py -> {fqdn}")
        try:
            subprocess.run([f'python3 toolkit/fire-cloud.py -S {args.server} -P {args.port} -d {fqdn}'], shell=True)
        except Exception as e:
            print(f"[!] Exception: {e}")

def scan_single_domain(args, logger, fqdn):
    if fqdn not in args.blacklist:
        print(f"[-] Running Drifting-Embers Modules (Vuln Scanning) against targeted domain: {fqdn}")
        logger.write_to_log("[MSG]", "Wildfire.py", f"Running Fire-Scanner.py -> {fqdn}")
        try:
            subprocess.run([f'python3 toolkit/fire-scanner.py -S {args.server} -P {args.port} -d {fqdn}'], shell=True)
        except Exception as e:
            print(f"[!] Exception: {e}")

def start(args, logger):
    res = get_fqdns(args)
    fqdn_json = json.loads(res.text)
    sorted_fqdns = sort_fqdns(fqdn_json)
    for fqdn in sorted_fqdns:
        if len(fqdn['recon']['subdomains']['httprobe']) > 1 and args.bridge:
            print(f"[!] Bridge-the-Gap Mode Detected!  Fire Starter has already been run against {fqdn['fqdn']}.  Skipping...")
            continue
        if fqdn['fqdn'] not in args.blacklist:
            if args.targeted:
                seed = args.targeted
                print(f"[-] Running Fire-Starter Modules (Subdomain Recon) against a single target: {seed}")
                try:
                    subprocess.run([f'python3 toolkit/fire-starter.py -d {seed} -S {args.server} -P {args.port} -p {args.proxy}'], shell=True)
                except Exception as e:
                    print(f"[!] Exception: {e}")
                return True
            seed = fqdn['fqdn']
            print(f"[-] Running Fire-Starter Modules (Subdomain Recon) against {seed}")
            logger.write_to_log("[MSG]","Wildfire.py",f"Running Fire-Starter.py -> {seed}")
            if args.deep:
                try:
                    subprocess.run([f'python3 toolkit/fire-starter.py -d {seed} -S {args.server} -P {args.port} -p {args.proxy} --deep'], shell=True)
                except Exception as e:
                    print(f"[!] Exception: {e}")
            if args.timeout:
                try:
                    subprocess.run([f'python3 toolkit/fire-starter.py -d {seed} -S {args.server} -P {args.port} -p {args.proxy} -t {args.timeout}'], shell=True)
                except Exception as e:
                    print(f"[!] Exception: {e}")
            else:
                try:
                    subprocess.run([f'python3 toolkit/fire-starter.py -d {seed} -S {args.server} -P {args.port} -p {args.proxy}'], shell=True)
                except Exception as e:
                    print(f"[!] Exception: {e}")
        else:
            print(f"[!] {fqdn['fqdn']} has been blacklisted for this round of scanning.  Skipping...")
    clean_screenshots(args)
    return True

def spread(args):
    print("[!] WARNING: The Fire-Spreader Module is still being developed.  PLEASE MAKE SURE THE SERVERs/PORTs ARE IN SCOPE FOR YOUR PROJECT BEFORE RUNNING --scan")
    sleep(5)
    res = get_fqdns(args)
    fqdn_json = json.loads(res.text)
    sorted_fqdns = sort_fqdns(fqdn_json)
    for fqdn in sorted_fqdns:
        if fqdn['fqdn'] not in args.blacklist:
            if args.targeted:
                seed = args.targeted
                print(f"[-] Running Fire-Spreader Modules (Server/Port Recon) against a single target: {seed}")
                try:
                    subprocess.run([f'python3 toolkit/fire-spreader.py -d {seed} -s {args.server} -p {args.port}'], shell=True)
                except Exception as e:
                    print(f"[!] Exception: {e}")
                try:
                    subprocess.run([f'python3 toolkit/wind.py -d {seed} -s {args.server} -p {args.port}'], shell=True)
                except Exception as e:
                    print(f"[!] Exception: {e}")
                return True
            seed = fqdn['fqdn']
            print(f"[-] Running Fire-Spreader Modules (Server/Port Recon) against {seed}")
            try:
                subprocess.run([f'python3 toolkit/fire-spreader.py -d {seed} -s {args.server} -p {args.port}'], shell=True)
            except Exception as e:
                    print(f"[!] Exception: {e}")
            # try:        
            #     subprocess.run([f'python3 toolkit/firewood.py -d {seed} -s {args.server} -p {args.port}'], shell=True)
            # except Exception as e:
            #         print(f"[!] Exception: {e}")
            try:
                subprocess.run([f'python3 toolkit/wind.py -d {seed} -s {args.server} -p {args.port}'], shell=True)
            except Exception as e:
                    print(f"[!] Exception: {e}")
        else:
            print(f"[!] {fqdn['fqdn']} has been blacklisted for this round of scanning.  Skipping...")
    return True

def cloud(args, logger):
    res = get_fqdns(args)
    fqdn_json = json.loads(res.text)
    sorted_fqdns = sort_fqdns(fqdn_json)
    for fqdn in sorted_fqdns:
        if fqdn['fqdn'] not in args.blacklist:
            if args.targeted:
                seed = args.targeted
                print(f"[-] Running Fire-Cloud Modules against a single target: {seed}")
                try:
                    subprocess.run([f'python3 toolkit/fire-cloud.py -S {args.server} -P {args.port} -d {seed}'], shell=True)
                except Exception as e:
                    print(f"[!] Exception: {e}")
                return True
            seed = fqdn['fqdn']
            print(f"[-] Running Fire-Cloud Modules against {seed}")
            logger.write_to_log("[MSG]","Wildfire.py",f"Running Fire-Cloud.py -> {seed}")
            try:
                subprocess.run([f'python3 toolkit/fire-cloud.py -S {args.server} -P {args.port} -d {seed}'], shell=True)
            except Exception as e:
                    print(f"[!] Exception: {e}")
        else:
            print(f"[!] {fqdn['fqdn']} has been blacklisted for this round of scanning.  Skipping...")
    return True

def scan(args, logger):
    res = get_fqdns(args)
    fqdn_json = json.loads(res.text)
    sorted_fqdns = sort_fqdns(fqdn_json)
    for fqdn in sorted_fqdns:
        if fqdn['fqdn'] not in args.blacklist:
            if args.targeted:
                seed = args.targeted
                print(f"[-] Running Drifting-Embers Modules (Vuln Scanning) against a single target: {seed}")
                try:
                    subprocess.run([f'python3 toolkit/fire-scanner.py -S {args.server} -P {args.port} -d {seed}'], shell=True)
                except Exception as e:
                    print(f"[!] Exception: {e}")
                return True
            seed = fqdn['fqdn']
            print(f"[-] Running Drifting-Embers Modules (Vuln Scanning) against {seed}")
            logger.write_to_log("[MSG]","Wildfire.py",f"Running Fire-Scanner.py -> {seed}")
            try:
                subprocess.run([f'python3 toolkit/fire-scanner.py -S {args.server} -P {args.port} -d {seed}'], shell=True)
            except Exception as e:
                    print(f"[!] Exception: {e}")
            # try:
            #     subprocess.run([f'python3 toolkit/proto_pollution_embers.py -d {seed} -s {args.server} -p {args.port} -T 2'], shell=True)
            # except Exception as e:
            #         print(f"[!] Exception: {e}")
            # try:
            #     subprocess.run([f'python3 toolkit/cve_embers.py -D {seed} -S {args.server} -P {args.port} -j -d 1'], shell=True)
            # except Exception as e:
            #         print(f"[!] Exception: {e}")
        else:
            print(f"[!] {fqdn['fqdn']} has been blacklisted for this round of scanning.  Skipping...")
    return True

def enum(args):
    print("[!] WARNING: The Enumeration Module is still VERY new and not very effective! Use at your own risk and don't expect much...")
    sleep(5)
    res = get_fqdns(args)
    fqdn_json = json.loads(res.text)
    sorted_fqdns = sort_fqdns(fqdn_json)
    for fqdn in sorted_fqdns:
        if fqdn['fqdn'] not in args.blacklist:
            if args.targeted:
                seed = args.targeted
                print(f"[-] Running Enumeration Modules against a single target: {seed}")
                try:
                    subprocess.run([f'python3 toolkit/ignite.py -d {seed} -s {args.server} -p {args.port} -P {args.proxy}'], shell=True)
                except Exception as e:
                    print(f"[!] Exception: {e}")
                return True
            try:
                subprocess.run([f'python3 toolkit/engulf.py -d {seed} -s {args.server} -p {args.port}'], shell=True)
            except Exception as e:
                    print(f"[!] Exception: {e}")
            seed = fqdn['fqdn']
            print(f"[-] Running Enumeration Modules against {seed}")
            try:
                subprocess.run([f'python3 toolkit/ignite.py -d {seed} -s {args.server} -p {args.port} -P {args.proxy}'], shell=True)
            except Exception as e:
                    print(f"[!] Exception: {e}")
            try:
                subprocess.run([f'python3 toolkit/engulf.py -d {seed} -s {args.server} -p {args.port}'], shell=True)
            except Exception as e:
                    print(f"[!] Exception: {e}")
        else:
            print(f"[!] {fqdn['fqdn']} has been blacklisted for this round of scanning.  Skipping...")
    return True

def build_blacklist(args):
    if "," in args.blacklist:
        blacklist_arr = args.blacklist.split(",")
    else:
        blacklist_arr = [args.blacklist]
    for i in range(0,len(blacklist_arr)):
        blacklist_arr[i] = blacklist_arr[i].strip()
    args.blacklist = blacklist_arr
    return args

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=False, default="127.0.0.1")
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=False, default="8000")
    parser.add_argument('-p','--proxy', help='IP Address of Burp Suite Proxy', required=False)
    parser.add_argument('-b','--blacklist', help='FQDN to Blacklist (skip) for this round of testing.  Separate multiple FQDNs w/ a comma (Ex: -b example1.com,example2.com)', required=False)
    parser.add_argument('--targeted', help='Runs the chosen Wildfire Scripts against a single domain', required=False)
    parser.add_argument('--start', help='Run Fire-Starter Modules', required=False, action='store_true')
    parser.add_argument('--spread', help='Run Fire-Spreader Modules (Expect a LONG scan time)', required=False, action='store_true')
    parser.add_argument('--scan', help='Run Vuln Scan Modules', required=False, action='store_true')
    parser.add_argument('--enum', help='Run Enumeration Modules', required=False, action='store_true')
    parser.add_argument('--cloud', help='Run Cloud Enumeration Modules', required=False, action='store_true')
    parser.add_argument('--deep', help='Crawl all live servers for subdomains', required=False, action='store_true')
    parser.add_argument('--bridge', help='Bridge-the-Gap Mode -- Only performs the Firestarter Module on a target FQDN if that module has not yet been run against that target', required=False, action='store_true')
    parser.add_argument('-t','--timeout', help='Adds a timeout check after each module (in minutes)', required=False)
    parser.add_argument('--fqdn', help='FQDN to target for scanning', required=False)
    parser.add_argument('--scanSingle', help='Flag to scan a single domain', required=False, action='store_true')
    return parser.parse_args()

def main(args):
    logger = Logger()
    if (args.blacklist):
        args = build_blacklist(args)
    else:
        args.blacklist = ""
    if not args.proxy:
        args.proxy = "127.0.0.1"
    wildfire_timer = Timer()
    if args.scanSingle and args.fqdn:
        if args.start:
            logger.write_to_log("[MSG]","Single Scan Wildfire.py","Start Flag Detected")
            start_single_domain(args, logger, args.fqdn)
        if args.cloud:
            logger.write_to_log("[MSG]","Single Scan Wildfire.py","Cloud Flag Detected")
            cloud_single_domain(args, logger, args.fqdn)
        if args.scan:
            logger.write_to_log("[MSG]","Single Scan Wildfire.py","Scan Flag Detected")
            scan_single_domain(args, logger, args.fqdn)
    else:
        if args.start:
            logger.write_to_log("[MSG]","Wildfire.py","Start Flag Detected")
            start(args, logger)
        if args.cloud:
            logger.write_to_log("[MSG]","Wildfire.py","Cloud Flag Detected")
            cloud(args, logger)
        if args.scan:
            logger.write_to_log("[MSG]","Wildfire.py","Scan Flag Detected")
            scan(args, logger)
    wildfire_timer.stop_timer()
    logger.create_datebase_log(args)
    logger.write_to_log("[DONE]","Wildfire.py","Wildfire Completed Successfully")
    print(f"[+] Wildfire Scan Done!  Start: {wildfire_timer.get_start()}  |  Stop: {wildfire_timer.get_stop()}")

if __name__ == "__main__":
    args = arg_parse()
    main(args)