import requests, sys, subprocess, getopt, json, time, math
import argparse
from datetime import datetime
import re

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

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    home_dir = get_home_dir.stdout.replace("\n", "")
    return home_dir

def get_fqdn_list(args):
    server_ip = args.server
    server_port = args.port
    res = requests.post(f'http://{server_ip}:{server_port}/api/auto', data={'fqdn':args.domain})
    thisFqdn = res.json()
    return thisFqdn

def dnsmasscan_install():
    home_dir = get_home_dir()
    initial_check = subprocess.run([f"ls {home_dir}/Tools/dnmasscan"], shell=True)
    if initial_check.returncode == 0:
        print("[+] Dnmasscan is installed")
    else :
        print("[!] Dnmasscan is NOT installed -- Installing now...")
        subprocess.run([f"cd {home_dir}/Tools; git clone https://github.com/rastating/dnmasscan.git;"], shell=True)
        print("[+] Dnmasscan was successfully installed")

def masscan_install():
    home_dir = get_home_dir()
    initial_check_two = subprocess.run([f"ls {home_dir}/Tools/masscan"], shell=True)
    if initial_check_two.returncode == 0:
        print("[+] Masscan is installed")
    else :
        print("[!] Masscan is NOT installed -- Installing now...")
        subprocess.run([f"cd {home_dir}/Tools; sudo apt-get --assume-yes install git make gcc; git clone https://github.com/robertdavidgraham/masscan; cd masscan; make; make install;"], shell=True)
        print("[+] Masscan was successfully installed")

def write_subdomain_file(subdomainArr):
    consolidatedStr = ""
    for subdomain in subdomainArr:
        if subdomain[0] == ".":
            modified_subdomain = subdomain[1:]
            consolidatedStr += f"{modified_subdomain}\n"
        else:
            consolidatedStr += f"{subdomain}\n"
    f = open("/tmp/dnmasscan.tmp", "w")
    f.write(consolidatedStr)
    f.close()

def main(args):
    home_dir = get_home_dir()
    thisFqdn = get_fqdn_list(args)
    subdomainArr = thisFqdn['recon']['subdomains']['consolidated']
    old_masscan_arr = thisFqdn['recon']['subdomains']['masscan']
    if args.install:
        dnsmasscan_install()
        masscan_install()
    print("[-] Running dnmasscan against consolidated server list...")
    write_subdomain_file(subdomainArr)
    dnmasscan_results = subprocess.run([f"cd {home_dir}/Tools/dnmasscan; sudo ./dnmasscan /tmp/dnmasscan.tmp /tmp/dns.log -p1-65535 -oJ /tmp/masscan.json --rate=100000"], stderr=subprocess.PIPE, text=True, shell=True)
    if "FAIL" in dnmasscan_results.stderr:
        print("[!] Masscan failed!  Attempting to fix the issue...")
        subprocess.run(["sed -i '1d' /tmp/dnmasscan.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run([f"cd {home_dir}/Tools/dnmasscan; sudo ./dnmasscan /tmp/dnmasscan.tmp /tmp/dns.log -p1-65535 -oJ /tmp/masscan.json --rate=100000"], shell=True)
    # subprocess.run(["rm /tmp/dnmasscan.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    f = open("/tmp/masscan.json", "r")
    data = f.read()
    if len(data) < 1:
        print("[!] DNMasscan returned no results.  Exiting...")
    else:
        masscan_data = json.loads(data)
        f.close()
        print("[+] Dnmasscan completed successfully!")
        print("[-] Packaging data for database...")
        data_arr = []
        for server in masscan_data:
            data_arr.append(f"{server['ip']}:{server['ports'][0]['port']}")
        thisFqdn['recon']['subdomains']['masscan'] = data_arr
        added = []
        removed = []
        for server in data_arr:
            if server not in old_masscan_arr:
                added.append(server)
        for server in old_masscan_arr:
            if server not in data_arr:
                removed.append(server)
        thisFqdn['recon']['subdomains']['masscanAdded'] = added
        thisFqdn['recon']['subdomains']['masscanRemoved'] = removed
        server_ip = args.server
        server_port = args.port
        r = requests.post(f'http://{server_ip}:{server_port}/api/auto/update', json=thisFqdn, headers={'Content-type':'application/json'})
        if r.status_code == 200:
            print("[+] Fire-Spreader Modules completed successfully!")
        else:
            print("[!] Fire-Spreader Modules did NOT complete successfully!")

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--server', help='IP Address of MongoDB API', required=True)
    parser.add_argument('-p','--port', help='Port of MongoDB API', required=True)
    parser.add_argument('-d','--domain', help='Target FQDN', required=True)
    parser.add_argument('--install', help='Install dnmasscan and masscan', required=False, action='store_true')    
    return parser.parse_args()

if __name__ == "__main__":
    args = arg_parse()
    main(args)