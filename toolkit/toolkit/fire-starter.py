import requests
import subprocess
import argparse
import json
import re
from datetime import datetime, timedelta
from time import sleep

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
            running_script = "Fire-Starter.py"
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

def update_scan_progress(scan_step_name, target_domain):
    requests.post("http://localhost:5000/update-scan", json={"stepName":scan_step_name,"target_domain":target_domain})

def sublist3r(args, home_dir, thisFqdn, logger):
    try:
        subprocess.run([f"python3 {home_dir}/Tools/Sublist3r/sublist3r.py -d {args.fqdn} -t 50 -o ./temp/sublist3r.tmp"], text=True, shell=True)
        f = open("./temp/sublist3r.tmp", "r")
        sublist3r_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm ./temp/sublist3r.tmp"], stdout=subprocess.DEVNULL, shell=True)
        thisFqdn['recon']['subdomains']['sublist3r'] = sublist3r_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['sublist3r'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Sublist3r Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        if """[Errno 2] No such file or directory: './temp/sublist3r.tmp'""" not in str(e):
            print(f"[!] Something went wrong!  Exception: {str(e)}")
            logger.write_to_log("[ERROR]","Fire-Starter.py",f"Sublist3r Exception: {str(e)}")
        else:
            print("[-] Sublist3r did not find any results.  Continuing scan...")

def remove_duplicate_ips(ip_list):
    try:
        clean_ip_list = []
        for ip in ip_list:
            if ip in clean_ip_list:
                continue
            clean_ip_list.append(ip)            
        return clean_ip_list
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

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

def amass_get_dns(args):
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

def amass(args, initFqdn, logger):
    try:
        config_test = subprocess.run(["ls config/amass_config.yaml"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if config_test.returncode == 0:
            print("[+] Amass config file detected!  Scanning with custom settings...")
            subprocess.run([f"amass enum -active -alts -brute -nocolor -min-for-recursive 2 -timeout 60 -config config/amass_config.yaml -d {args.fqdn} -o ./temp/amass.tmp"], shell=True)
        else:
            print("[!] Amass config file NOT detected!  Scanning with default settings...")
            subprocess.run([f"amass enum -active -alts -brute -nocolor -min-for-recursive 2 -timeout 60 -d {args.fqdn} -o ./temp/amass.tmp"], shell=True)
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
        thisFqdn['dns'] = amass_get_dns(args)
        final_amass_arr = []
        for amass_finding in amass_arr:
            if thisFqdn['fqdn'] in amass_finding and amass_finding not in final_amass_arr:
                final_amass_arr.append(amass_finding)
        thisFqdn['recon']['subdomains']['amass'] = final_amass_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['amass'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Amass Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"Amass Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def assetfinder(args, home_dir, thisFqdn, logger):
    try:
        subprocess.run([f"{home_dir}/go/bin/assetfinder --subs-only {args.fqdn} > ./temp/assetfinder.tmp"], shell=True)
        f = open(f"./temp/assetfinder.tmp", "r")
        assetfinder_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm ./temp/assetfinder.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['assetfinder'] = assetfinder_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['assetfinder'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Assetfinder Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"Assetfinder Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def gau(args, home_dir, thisFqdn, logger):
    try:
        subprocess.run([f"{home_dir}/go/bin/gau --subs {args.fqdn} | cut -d / -f 3 | sort -u > ./temp/gau.tmp"], shell=True)
        f = open(f"./temp/gau.tmp", "r")
        gau_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm ./temp/gau.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['gau'] = gau_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['gau'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"GAU Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"GAU Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def crt(args, home_dir, thisFqdn, logger):
    try:
        subprocess.run([f"{home_dir}/Tools/tlshelpers/getsubdomain {args.fqdn} > ./temp/ctl.tmp"], shell=True)
        f = open(f"./temp/ctl.tmp", "r")
        ctl_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm ./temp/ctl.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['ctl'] = ctl_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['ctl'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"CTL Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"CTL Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def subfinder(args, home_dir, thisFqdn, logger):
    try:
        subprocess.run([f'{home_dir}/go/bin/subfinder -d {args.fqdn} -o ./temp/subfinder.tmp'], shell=True)
        f = open(f"./temp/subfinder.tmp", "r")
        subfinder_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm -rf ./temp/subfinder.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['subfinder'] = subfinder_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['subfinder'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Subfinder Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"Subfinder Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def subfinder_recursive(args, home_dir, thisFqdn, logger):
    try:
        subprocess.run([f'{home_dir}/go/bin/subfinder -d {args.fqdn} -recursive -o ./temp/subfinder.tmp'], shell=True)
        f = open(f"./temp/subfinder.tmp", "r")
        subfinder_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm -rf ./temp/subfinder.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        combined_subfinder_results = list(set(subfinder_arr + thisFqdn['recon']['subdomains']['subfinder']))
        thisFqdn['recon']['subdomains']['subfinder'] = combined_subfinder_results
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(subfinder_arr)
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Subfinder (Recursive) Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"Subfinder (Recursive) Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def gospider(args, home_dir, thisFqdn, logger):
    try:
        subprocess.run([f'echo "https://{args.fqdn}" | {home_dir}/go/bin/gospider -o ./temp/gospider -c 10 -d 1 --other-source --subs --include-subs'], shell=True)
        fqdn = args.fqdn
        outputFile = fqdn.replace(".", "_")
        f = open(f"./temp/gospider/{outputFile}", "r")
        gospider_arr = f.read().rstrip().split("\n")
        gospider_link_arr = []
        for line in gospider_arr:
            new_arr = line.split(" ")
            if len(new_arr) > 2:
                temp_arr = new_arr[2].split("/")
                if len(temp_arr) > 2:
                    if temp_arr[2] not in gospider_link_arr:
                        gospider_link_arr.append(temp_arr[2])
        f.close()
        subprocess.run(["rm -rf ./temp/gospider"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        for item in gospider_link_arr:
            if args.fqdn not in item:
                gospider_link_arr.remove(item)
        thisFqdn['recon']['subdomains']['gospider'] = gospider_link_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['gospider'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"GoSpider Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"GoSpider Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def gospider_deep(home_dir, thisFqdn, logger):
    try:
        f = open('wordlists/crawl_list.tmp', 'r')
        domain_arr = f.read().rstrip().split("\n")
        for domain in domain_arr:
            subprocess.run([f'{home_dir}/go/bin/gospider -S ./wordlists/live_servers.txt -o ./temp/gospider -c 10 -d 1 --other-source --subs --include-subs'], shell=True)
            fqdn = domain.split("/")[2]
            outputFile = fqdn.replace(".", "_")
            f = open(f"./temp/gospider/{outputFile}", "r")
            gospider_arr = f.read().rstrip().split("\n")
            gospider_link_arr = []
            for line in gospider_arr:
                new_arr = line.split(" ")
                if len(new_arr) > 2:
                    temp_arr = new_arr[2].split("/")
                    if len(temp_arr) > 2:
                        if temp_arr[2] not in gospider_link_arr:
                            gospider_link_arr.append(temp_arr[2])
            f.close()
        subprocess.run(["rm -rf ./temp/gospider"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['gospider'] = gospider_link_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['gospider'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"GoSpider Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"GoSpider Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def subdomainizer(home_dir, thisFqdn, logger):
    try:
        file_path = './wordlists/live_servers.txt'
        max_lines = 250
        with open(file_path, 'r') as file:
            lines = file.readlines()
        line_count = len(lines)
        if line_count > max_lines:
            with open(file_path, 'w') as file:
                file.writelines(lines[:max_lines])
        subprocess.run([f"""timeout 4h python3 {home_dir}/Tools/SubDomainizer/SubDomainizer.py -l ./wordlists/live_servers.txt -o ./temp/subdomainizer.tmp -sop ./temp/secrets.tmp;if [ -f "./temp/secrets.tmp" ]; then cp ./temp/secrets.tmp /tmp; fi"""], shell=True)
        try:
            f = open("./temp/subdomainizer.tmp", "r")
            subdomainizer_arr = f.read().rstrip().split("\n")
            f.close()
            subprocess.run(["rm ./temp/subdomainizer.tmp"], stdout=subprocess.DEVNULL, shell=True)
        except Exception as e:
            print("[!] Subdomainzier Timed Out!  Skipping...")
            logger.write_to_log("[ERROR]","Fire-Starter.py",f"[!] Subdomainzier Timed Out!  Skipping...")
            subdomainizer_arr = []
        thisFqdn['recon']['subdomains']['subdomainizer'] = subdomainizer_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['subdomainizer'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Subdomainizer Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"Subdomainizer Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def shuffle_dns(args, home_dir, thisFqdn, logger):
    try:
        subprocess.run([f'echo {args.fqdn} | {home_dir}/go/bin/shuffledns -w wordlists/all.txt -r wordlists/resolvers.txt -o ./temp/shuffledns.tmp'], shell=True)
        f = open(f"./temp/shuffledns.tmp", "r")
        shuffledns_arr = f.read().rstrip().split("\n")
        for subdomain in shuffledns_arr:
            if args.fqdn not in subdomain and subdomain != "":
                i = shuffledns_arr.index(subdomain)
                del shuffledns_arr[i]
        f.close()
        subprocess.run(["rm -rf ./temp/shuffledns.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['shuffledns'] = shuffledns_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['shuffledns'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"ShuffleDNS (Default) Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"ShuffleDNS (Default) Exception: {str(e)}")
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def shuffle_dns_custom(args, home_dir, thisFqdn, logger):
    try:
        subprocess.run([f'echo {args.fqdn} | {home_dir}/go/bin/shuffledns -w wordlists/cewl_{args.fqdn}.txt -r wordlists/resolvers.txt -o ./temp/shuffledns_custom.tmp'], shell=True)
        try:
            f = open(f"./temp/shuffledns_custom.tmp", "r")
        except:
            print("[!] No results found from the CeWL scan.  Skipping the 2nd round of ShuffleDNS...")
            return False
        shuffledns_custom_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm -rf ./temp/shuffledns_custom.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        clean_shuffledns_custom_arr = [item for item in shuffledns_custom_arr if item != ""]
        thisFqdn['recon']['subdomains']['shufflednsCustom'] = clean_shuffledns_custom_arr
        update_fqdn_obj(args, thisFqdn)
        subdomains_found = len(thisFqdn['recon']['subdomains']['shufflednsCustom'])
        logger.write_to_log("[MSG]","Fire-Starter.py",f"ShuffleDNS (Custom) Completed Successfully: {subdomains_found} Results Found")
    except Exception as e:
        logger.write_to_log("[WARN]","Fire-Starter.py",f"ShuffleDNS (Custom) Exception: {str(e)}")
        print(f"[!] ShuffleDNS w/ Custom Wordlist Failed!\n[!] Exception: {str(e)}")

def consolidate(args):
    thisFqdn = get_fqdn_obj(args)
    consolidated = []
    consolidatedNew = []
    for key in thisFqdn['recon']['subdomains']:
        for subdomain in thisFqdn['recon']['subdomains'][key]:
            if subdomain in thisFqdn['recon']['subdomains']['httprobe']:
                continue
            if subdomain in thisFqdn['recon']['subdomains']['httprobeAdded']:
                continue
            if subdomain in thisFqdn['recon']['subdomains']['httprobeRemoved']:
                continue
            if subdomain not in thisFqdn['recon']['subdomains']['consolidated'] and args.fqdn in subdomain and "?" not in subdomain and "http" not in subdomain:
                consolidatedNew.append(subdomain)
            if args.fqdn in subdomain and "?" not in subdomain and "http" not in subdomain:
                consolidated.append(subdomain)
    thisFqdn['recon']['subdomains']['consolidated'] = set(consolidated)
    thisFqdn['recon']['subdomains']['consolidatedNew'] = consolidatedNew
    temp = []
    for subdomain in thisFqdn['recon']['subdomains']['consolidated']:
        if "?" not in subdomain:
            temp.append(subdomain)
    thisFqdn['recon']['subdomains']['consolidated'] = temp
    temp = []
    for subdomain in thisFqdn['recon']['subdomains']['consolidatedNew']:
        if "?" not in subdomain:
            temp.append(subdomain)
    thisFqdn['recon']['subdomains']['consolidatedNew'] = temp
    update_fqdn_obj(args, thisFqdn)

def httprobe(args, home_dir, thisFqdn):
    subdomainStr = ""
    subdomainArr = thisFqdn['recon']['subdomains']['consolidated']
    for subdomain in subdomainArr:
        subdomainStr += f"{subdomain}\n"
    f = open("./temp/consolidated_list.tmp", "w")
    f.write(subdomainStr)
    f.close()
    httprobe_results = subprocess.run([f"cat ./temp/consolidated_list.tmp | {home_dir}/go/bin/httprobe -t 8000 -c 500 -p http:8080 -p http:8000 -p http:8008 -p https:8443 -p https:44300 -p https:44301"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    thisFqdn = r.json()
    httprobe_stdout = httprobe_results.stdout
    httprobe_stderr = httprobe_results.stderr
    httprobe = httprobe_stdout.split("\n")
    for item in httprobe:
        if len(item) < 2:
            httprobe.remove(item)
    previous_httprobe = thisFqdn['recon']['subdomains']['httprobe']
    httprobeAdded = []
    httprobeRemoved = []
    for subdomain in httprobe:
        if subdomain not in previous_httprobe:
            httprobeAdded.append(subdomain)
    for subdomain in previous_httprobe:
        if subdomain not in httprobe:
            httprobeRemoved.append(subdomain)
    thisFqdn['recon']['subdomains']['httprobe'] = remove_duplicates(httprobe)
    thisFqdn['recon']['subdomains']['httprobeAdded'] = remove_duplicates(httprobeAdded)
    thisFqdn['recon']['subdomains']['httprobeRemoved'] = remove_duplicates(httprobeRemoved)
    # sleep(60)
    update_fqdn_obj(args, thisFqdn)

def remove_duplicates(string_list):
    return list(set(string_list))

def build_crawl_list(thisFqdn):
    live_servers = thisFqdn['recon']['subdomains']['httprobe']
    f = open('./wordlists/live_servers.txt', 'w')
    for domain in live_servers:
        f.write(f"{domain}\n")
    f.close()

# Clear Sky

def get_aws_ip_ranges():
    subprocess.run([f"wget -O wordlists/aws-ip-ranges.json https://ip-ranges.amazonaws.com/ip-ranges.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    f = open(f'wordlists/aws-ip-ranges.json')
    aws_ips = json.load(f)
    ip_ranges = []
    ip_ranges_str = ""
    for ip_range in aws_ips['prefixes']:
        ip_ranges.append(ip_range['ip_prefix'])
        ip_ranges_str += f"{ip_range['ip_prefix']}\n"
    f.close()
    f = open("wordlists/aws_ips.txt", "w")
    f.write(ip_ranges_str)
    f.close()

def identify_hosts():
    ip_count = subprocess.run([f"nmap -n -sL -iL wordlists/aws_ips.txt | wc -l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return ip_count.stdout.replace("\n", "")

def masscan_to_tls(home_dir):
    subprocess.run([f"sudo masscan -p443 --rate 40000 -iL wordlists/aws_ips.txt -oL ./temp/clear_sky_masscan.tmp"], shell=True)
    subprocess.run(["cat ./temp/clear_sky_masscan.tmp | awk {'print $4'} | awk NF | sort -u > ./temp/tls-scan-in.tmp"], shell=True)
    subprocess.run([f"cat ./temp/tls-scan-in.tmp | {home_dir}/Tools/tls-scan/tls-scan --port=443 --concurrency=150 --cacert={home_dir}/Tools/tls-scan/ca-bundle.crt 2>/dev/null -o wordlists/tls-results.json"], shell=True)

def update_aws_domains():
    try:
        get_aws_ip_ranges()
        ip_count = identify_hosts()
        print(f"[-] Running masscan -> tls-scan against {ip_count} IPs...")
        masscan_to_tls(get_home_dir())
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def check_clear_sky_data():
    document_check = subprocess.run([f"ls wordlists/tls-results.json"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, shell=True)
    if document_check.returncode == 0:
        return True
    else:
        return False

def search_data(args, thisFqdn):
    subprocess.run([f"""cat wordlists/tls-results.json | jq --slurp -r '.[]? | select(.certificateChain[]?.subject | test("{args.fqdn}")) | .ip | @text' > wordlists/tls_filtered.tmp"""], shell=True)
    results_str = subprocess.run([f"cat wordlists/tls_filtered.tmp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    results_arr = results_str.stdout.split("\n").pop()
    # if len(results_arr) < 10:
    #     subprocess.run([f"sudo nmap -T 4 -iL wordlists/tls_filtered.tmp -Pn --script=http-title -p- --open -oN reports/Clear-Sky_{args.search}_{now}"], shell=True)
    # else:
    #     subprocess.run([f"sudo nmap -T 4 -iL wordlists/tls_filtered.tmp -Pn --script=http-title -p- --open -oN reports/Clear-Sky_{args.search}_{now}"], shell=True)
    thisFqdn['recon']['subdomains']['cloudRanges'] = results_arr
    update_fqdn_obj(args, thisFqdn)

# End Clear Sky

def get_new_subdomain_length(args):
    thisFqdn = get_fqdn_obj(args)
    return len(thisFqdn['recon']['subdomains']['consolidatedNew'])

def send_slack_notification(home_dir, text):
    message_json = {'text':text,'username':'Recon Box','icon_emoji':':eyes:'}
    f = open(f'{home_dir}/.keys/slack_web_hook')
    token = f.read()
    clean_token = token.replace(u"\u000a","")
    requests.post(f'https://hooks.slack.com/services/{clean_token}', json=message_json)

def build_cewl_wordlist(args, logger):
    try:
        subprocess.run([f'ls; cewl -d 2 -m 5 -o -a -v -w wordlists/cewl_{args.fqdn}.txt https://{args.fqdn}'], shell=True)
    except Exception as e:
        logger.write_to_log("[WARN]","Fire-Starter.py",f"CeWL Failed to Build Custom Wordlist! -> {args.fqdn}")

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def get_fqdn_obj(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    return r.json()

def update_fqdn_obj(args, thisFqdn):
    res = requests.post(f'http://{args.server}:{args.port}/api/auto/update', json=thisFqdn)

def cleanup():
    subprocess.run(["rm wordlists/crawl_*"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["rm wordlists/cewl_*"],  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["rm wordlists/live_*"],  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["rm temp/*.tmp"],  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["rm log/nuclei*.dump"],  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def get_live_server_text(args, thisFqdn, first):
    if first is True:
        context_str = "Starting second round of recon..."
    else:
        context_str = "Happy Hunting :)"
    length = len(thisFqdn['recon']['subdomains']['httprobeAdded'])
    if length > 10:
        return f'This scan of {args.fqdn} discovered that {length} URLs went live since the last scan!  {context_str}'
    elif length < 1:
        if first:
            return f'This scan of {args.fqdn} did not find any new live URLs.  Starting second round of recon...'
        return f'This scan of {args.fqdn} did not find any new live URLs.  Better luck next time :('
    else:
        message_urls_string = ""
        for url in thisFqdn['recon']['subdomains']['httprobeAdded']:
            message_urls_string += f"{url}\n"
        return f'This scan of {args.fqdn} discovered the following URLs went live since the last scan:\n\n{message_urls_string}\nHappy Hunting :)'

def populate_burp(args, thisFqdn):
    url_list = thisFqdn['recon']['subdomains']['httprobe']
    f = open('./temp/populate_burp.tmp', 'w')
    for url in url_list:
        f.write(f'{url}\n')
    f.close()
    subprocess.run([f"ffuf -u 'FUZZ' -w ./temp/populate_burp.tmp -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36' -replay-proxy 'http://{args.proxy}:8080'"], shell=True)
    subprocess.run([f"rm ./temp/populate_burp.tmp"], shell=True)

def check_limit(args):
    thisFqdn = get_fqdn_obj(args)
    unique_domain_count = 0
    for lst in thisFqdn['recon']['subdomains']:
        unique_domain_count += len(thisFqdn['recon']['subdomains'][lst])
    if unique_domain_count > 2000:
        print("[!] Unique subdomain limit reached!  Ending the scan for now, but you can always come back and run the scan again without the -l|--limit flat.")
        wrap_up(args)
        exit()
    print(f"[+] Current unique subdomain count: {unique_domain_count}\n[+] Continuing scan...")

def check_timeout(args, timer):
    start_time = timer.start
    timeout_minutes = int(args.timeout)
    start_time += timedelta(minutes=timeout_minutes)
    timeout = start_time
    now = datetime.now()
    if now > timeout:
        print("[!] Current scan time has exceeded the timeout threshold!  Exiting Fire Starter Module...")
        wrap_up(args)
        exit()
    else:
        time_left = timeout - now
        print(F"[+] Time remaining before timeout threshold: {time_left}")

def validate_httprobe(args, thisFqdn):
    if len(thisFqdn['recon']['subdomains']['httprobe']) < 1:
        domain = thisFqdn['fqdn']
        slack_text = f'Something may have gone wrong with Httprobe!  Domain: {domain}'
        send_slack_notification(get_home_dir(), slack_text)
    for i in range(50):
        if len(thisFqdn['recon']['subdomains']['httprobe']) < 1:
            print(f"[!] Something may have gone wrong with Httprobe.\n[!] Sleeping for 2 minutes, then trying again...")
            sleep(120)
            httprobe(args, get_home_dir(), get_fqdn_obj(args))
        else:
            break

def wrap_up(args):
    consolidate(args)
    # new_subdomain_length = get_new_subdomain_length(args)
    # slack_text = f'The subdomain list for {args.fqdn} has been updated with {new_subdomain_length} new subdomains!'
    # send_slack_notification(get_home_dir(), slack_text)
    try:
        print(f"[-] Running Httprobe against {args.fqdn}")
        httprobe(args, get_home_dir(), get_fqdn_obj(args))
        validate_httprobe(args, get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    # input("[!] Debug Pause...")
    send_slack_notification(get_home_dir(), get_live_server_text(args, get_fqdn_obj(args), False))
    try:
        populate_burp(args, get_fqdn_obj(args))
    except Exception as e:
        print("[!] Burp Suite Proxy NOT Found.  Skipping Populate Burp Module...")
    cleanup()

def update_nuclei(logger):
    home_dir = get_home_dir()
    print("[-] Updating Nuclei and Nuclei Templates...")
    logger.write_to_log("[MSG]","Fire-Starter.py",f"Updating Nuclei...")
    try:
        subprocess.run([f'export PATH="$HOME/go/bin:$PATH"; {home_dir}/go/bin/nuclei -update -ut;'], shell=True)
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Nuclei Update Succesful!")
    except Exception as e:
        logger.write_to_log("[ERROR]","Fire-Starter.py",f"Nuclei Update Was NOT Successful!  Exception: {e}")

def collect_screenshots(home_dir, thisFqdn, logger):
    subprocess.run(["rm -f screenshots/*.png"], shell=True)
    with open('./temp/urls.txt', 'w') as file:
        for url in thisFqdn['recon']['subdomains']['httprobe']:
            file.write(url + '\n')
    update_nuclei(logger)
    subprocess.run([f"{home_dir}/go/bin/nuclei -t {home_dir}/nuclei-templates/headless/screenshot.yaml -l ./temp/urls.txt -stats -system-resolvers -config config/nuclei_config.yaml -vv --headless -sb -hbs 10 -headc 1 -fhr -hm"], shell=True)
    subprocess.run("""for file in ./screenshots/*; do cp -f "$file" "../client/public/screenshots/$(basename "$file")"; done""", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["rm -f screenshots/*.png"], shell=True)

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=True)
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=True)
    parser.add_argument('-d','--fqdn', help='Name of the Root/Seed FQDN', required=True)
    parser.add_argument('-p','--proxy', help='IP Address of Burp Suite Proxy', required=False, default="127.0.0.1")
    parser.add_argument('-t','--timeout', help='Adds a timeout check after each module (in minutes)', required=False)
    parser.add_argument('--deep', help='Crawl all live servers for subdomains', required=False, action='store_true')
    parser.add_argument('-u', '--update', help='Update AWS IP Certificate Data ( Can Take 48+ Hours! )', required=False, action='store_true')
    parser.add_argument('-l', '--limit', help='Stop the scan when the number of unique subdomains goes above 2000', required=False, action='store_true')
    parser.add_argument('-c', '--consolidate', help='Consolidate and Run HTTProbe Against Discovered Subdomains', required=False, action='store_true')
    parser.add_argument('-s', '--screenshots', help='Collect a new round of screenshots for all live URLs', required=False, action='store_true')
    return parser.parse_args()

def consolidate_flag(args):
    print("[-] Consolidate Flag Detected!  Running Wrap-Up Function...")
    wrap_up(args)
    print("[+] Wrap-Up Function Completed Successfully!  Exiting...")
    exit()

def run_checks(args, starter_timer):
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    # input("[!] Debug Pause...")

def protonvpn_connect():
    command = subprocess.run(["protonvpn-cli c -f"], shell=True)

def protonvpn_disconnect():
    command = subprocess.run(["protonvpn-cli d"], shell=True)

def protonvpn_status():
    command = subprocess.run(["protonvpn-cli s"], stdout=subprocess.PIPE, text=True, shell=True)
    return command.stdout
    
def protonvpn_killswitch():
    command = subprocess.run(["protonvpn-cli ks --permanent"], shell=True)

def main(args):
    args.limit = True
    starter_timer = Timer()
    # network_validator = NetworkValidator()
    logger = Logger()
    cleanup()
    print("[-] Running Subdomain Scraping Modules...")
    # Amass
    try:
        update_scan_progress("Fire-Starter | Amass", args.fqdn)
        print(f"[-] Running Amass against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running Amass -> {args.fqdn}")
        amass(args, get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")

    # Subdomain Scraping
    try:
        update_scan_progress("Fire-Starter | Sublist3r", args.fqdn)
        print(f"[-] Running Sublist3r against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running Sublist3r -> {args.fqdn}")
        sublist3r(args, get_home_dir(), get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")

    try:
        update_scan_progress("Fire-Starter | Assetfinder", args.fqdn)
        print(f"[-] Running Assetfinder against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running Assetfinder -> {args.fqdn}")
        assetfinder(args, get_home_dir(), get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")

    try:
        update_scan_progress("Fire-Starter | GAU", args.fqdn)
        print(f"[-] Running Get All URLs against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running GAU -> {args.fqdn}")
        gau(args, get_home_dir(), get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")

    try:
        update_scan_progress("Fire-Starter | CRT", args.fqdn)
        print(f"[-] Running CRT against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running CRT -> {args.fqdn}")
        crt(args, get_home_dir(), get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")

    try:
        update_scan_progress("Fire-Starter | Subfinder", args.fqdn)
        print(f"[-] Running Subfinder against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running Subfinder -> {args.fqdn}")
        subfinder(args, get_home_dir(), get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")

    try:
        update_scan_progress("Fire-Starter | Subfinder (Recursive)", args.fqdn)
        print(f"[-] Running Subfinder in Recursive Mode against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running Subfinder (Recursive) -> {args.fqdn}")
        subfinder_recursive(args, get_home_dir(), get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")

    # Subdomain Brute Force
    try:
        update_scan_progress("Fire-Starter | ShuffleDNS", args.fqdn)
        print(f"[-] Running ShuffleDNS w/ a Default Wordlist against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running ShuffleDNS (Default) -> {args.fqdn}")
        shuffle_dns(args, get_home_dir(), get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")

    try:
        update_scan_progress("Fire-Starter | ShuffleDNS (Custom)", args.fqdn)
        print(f"[-] Running CEWL against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Building CeWL Wordlist -> {args.fqdn}")
        build_cewl_wordlist(args, logger)
        print(f"[-] Running ShuffleDNS w/ a Custom Wordlist against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running ShuffleDNS (Custom) -> {args.fqdn}")
        shuffle_dns_custom(args, get_home_dir(), get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")
    
    wrap_up(args)
    build_crawl_list(get_fqdn_obj(args))

    # Subdomain Link/JS Discovery
    if args.deep:
        update_scan_progress("Fire-Starter | Gospider", args.fqdn)
        print(f"[-] Running DEEP Crawl Scan on {args.fqdn}...")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running GoSpider (Deep) -> {args.fqdn}")
        try:
            gospider_deep(get_home_dir(), get_fqdn_obj(args), logger)
            run_checks(args, starter_timer)
        except Exception as e:
            print(f"[!] Exception: {e}")
    else:
        try:
            update_scan_progress("Fire-Starter | Gospider", args.fqdn)
            print(f"[-] Running Gospider against {args.fqdn}")
            logger.write_to_log("[MSG]","Fire-Starter.py",f"Running GoSpider -> {args.fqdn}")
            gospider(args, get_home_dir(), get_fqdn_obj(args), logger)
            run_checks(args, starter_timer)
        except Exception as e:
            print(f"[!] Exception: {e}")

    try:
        update_scan_progress("Fire-Starter | Subdomainizer", args.fqdn)
        print(f"[-] Running Subdomainizer against {args.fqdn}")
        logger.write_to_log("[MSG]","Fire-Starter.py",f"Running Subdomainizer -> {args.fqdn}")
        print(f"[-] Current Time: {datetime.now()}")
        subdomainizer(get_home_dir(), get_fqdn_obj(args), logger)
        run_checks(args, starter_timer)
    except Exception as e:
        print(f"[!] Exception: {e}")

    if not check_clear_sky_data():
        if not args.update:
            logger.write_to_log("[MSG]","Fire-Starter.py",f"Clear Sky Data NOT Found.  Skipping...")
            print("[!] Clear Sky data not found!  Skipping AWS IP range scan...")
            print("[!] To enable the Clear Sky module, run fire-starter.py in UPDATE MODE (--update)")
        else:
            update_aws_domains()
    else:
        print(f"[-] Running Clear-Sky against {args.fqdn}")
        search_data(args, get_fqdn_obj(args))

    wrap_up(args)
    collect_screenshots(get_home_dir(), get_fqdn_obj(args), logger)
    starter_timer.stop_timer()
    logger.write_to_log("[DONE]","Fire-Starter.py",f"Fire-Starter Completed Successfully -> {args.fqdn}")
    print(f"[+] Fire Starter Modules Done!  Start: {starter_timer.get_start()}  |  Stop: {starter_timer.get_stop()}")

if __name__ == "__main__":
    args = arg_parse()
    if args.consolidate:
       consolidate_flag(args)
    if args.screenshots:
       collect_screenshots(get_home_dir(), get_fqdn_obj(args), logger = Logger())
       exit()
    main(args)