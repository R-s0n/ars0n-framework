import requests, sys, subprocess, getopt, json, time, math
import argparse
from datetime import datetime

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