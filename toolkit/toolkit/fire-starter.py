# ### Hakrawler
# 
# try:
#     hakrawler = subprocess.run([f"ls {home_dir}/go/bin/hakrawler"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
#     if hakrawler.returncode == 0:
#         print("[+] Hakrawler is already installed")
#     else :
#         print("[!] Hakrawler is NOT already installed -- Installing now...")
#         cloning = subprocess.run(["go install github.com/hakluke/hakrawler@latest"], stdout=subprocess.DEVNULL, shell=True)
#         print("[+] Hakrawler successfully installed!")
#     print(f"[-] Running Hakrawler against {fqdn}...")
#     # Add after debug: stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, 
#     subprocess.run([f'cd {home_dir}/go/bin; cat /tmp/amass.tmp | ./hakrawler -subs -d 3 -v > /tmp/hakrawler.tmp'], shell=True)
#     f = open(f"/tmp/hakrawler.tmp", "r")
#     hakrawler_arr = f.read().rstrip().split("\n")
#     hakrawler_link_arr = []
#     for line in hakrawler_arr:
#         new_arr = line.split(" ")
#         if len(new_arr) > 1:
#             temp_arr = new_arr[1].split("/")
#             if len(temp_arr) > 2:
#                 if temp_arr[2] not in hakrawler_link_arr:
#                     hakrawler_link_arr.append(temp_arr[2])
#     f.close()
#     subprocess.run(["rm -rf /tmp/hakrawler"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
#     print("[+] Hakwraler completed successfully!")
#     thisFqdn['recon']['subdomains']['hakrawler'] = hakrawler_link_arr
# except Exception as e:
#     print(f'[!] Exception: {e}')
#     print("[!] Hakrawler module did NOT complete successfully -- skipping...")


# eyewitness_check = httprobe_check = subprocess.run([f"ls {home_dir}/Tools/EyeWitness"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
# if httprobe_check.returncode == 0:
#     print("[+] EyeWitness is already installed")
# else :
#     print("[!] EyeWitness is NOT already installed -- Installing now...")
#     cloning = subprocess.run([f"cd {home_dir}/Tools; git clone https://github.com/FortyNorthSecurity/EyeWitness.git;  cd EyeWitness/Python/setup/;  sudo ./setup.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
#     print("[+] EyeWitness successfully installed!")
# httprobe_string = ""
# for subdomain in httprobe:
#     httprobe_string += f"{subdomain}\n"
# f = open("/tmp/httprobe_results.tmp", "w")
# f.write(httprobe_string)
# f.close()
# now = datetime.now().strftime("%d-%m-%y_%I%p")
# print(f"[-] Running EyeWitness report against {fqdn} httprobe results...")
# subprocess.run([f"rm -rf {home_dir}/Reports/EyeWitness_kindling_{fqdn}_*"], shell=True)
# subprocess.run([f"cd {home_dir}/Tools/EyeWitness/Python; ./EyeWitness.py -f /tmp/httprobe_results.tmp -d {home_dir}/Reports/EyeWitness_kindling_{fqdn}_{now} --no-prompt --jitter 5 --timeout 10"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
# print(f"[+] EyeWitness report complete!")


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

def sublist3r(args, home_dir, thisFqdn):
    try:
        subprocess.run([f"python3 {home_dir}/Tools/Sublist3r/sublist3r.py -d {args.fqdn} -t 50 -o /tmp/sublist3r.tmp"], text=True, shell=True)
        f = open("/tmp/sublist3r.tmp", "r")
        sublist3r_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm /tmp/sublist3r.tmp"], stdout=subprocess.DEVNULL, shell=True)
        thisFqdn['recon']['subdomains']['sublist3r'] = sublist3r_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

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

def get_ips_from_amass(thisFqdn):
    try:
        amass_file = open(f"/tmp/amass.tmp", 'r')
        amass_file_lines = amass_file.readlines()
        amass_file.close()
        ip_list = []
        for line in amass_file_lines:
            ip_string = line.strip().split(" ")[1]
            if "," in ip_string:
                new_ip_list = ip_string.split(",")
                for ip in new_ip_list:
                    if len(ip) > 4:
                        ip_obj = {
                            "ip": ip,
                            "ports": []
                        }
                        ip_list.append(ip_obj)
            else:
                ip_obj = {
                    "ip": ip_string,
                    "ports": []
                }
                ip_list.append(ip_obj)
        clean_ip_list = remove_duplicate_ips(ip_list)
        thisFqdn['ips'] = clean_ip_list
        return thisFqdn  
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def amass(args, thisFqdn):
    try:
        regex = "{1,3}"
        subprocess.run([f"amass enum -src -ip -brute -ipv4 -min-for-recursive 2 -timeout 60 -d {args.fqdn} -o /tmp/amass.tmp"], shell=True)
        subprocess.run([f"cp /tmp/amass.tmp /tmp/amass.full.tmp"], stdout=subprocess.DEVNULL, shell=True)
        subprocess.run([f"sed -i -E 's/\[(.*?)\] +//g' /tmp/amass.tmp"], stdout=subprocess.DEVNULL, shell=True)
        thisFqdn = get_ips_from_amass(thisFqdn)
        subprocess.run([f"sed -i -E 's/ ([0-9]{regex}\.)[0-9].*//g' /tmp/amass.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        amass_file = open(f"/tmp/amass.tmp", 'r')
        amass_file_lines = amass_file.readlines()
        amass_file.close()
        new_lines = []
        for line in amass_file_lines:
            if " " in line:
                subdomain = line.split(" ")[0] + "\n"
                new_lines.append(subdomain)
            else:
                new_lines.append(line)
        subprocess.run(["rm -rf /tmp/amass.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        amass_file = open(f"/tmp/amass.tmp", 'w')
        amass_file.writelines(new_lines)
        amass_file.close()
        f = open(f"/tmp/amass.tmp", "r")
        amass_arr = f.read().rstrip().split("\n")
        f.close()
        thisFqdn['recon']['subdomains']['amass'] = amass_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def assetfinder(args, home_dir, thisFqdn):
    try:
        subprocess.run([f"{home_dir}/go/bin/assetfinder --subs-only {args.fqdn} > /tmp/assetfinder.tmp"], shell=True)
        f = open(f"/tmp/assetfinder.tmp", "r")
        assetfinder_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm /tmp/assetfinder.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['assetfinder'] = assetfinder_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def gau(args, home_dir, thisFqdn):
    try:
        subprocess.run([f"{home_dir}/go/bin/gau --subs {args.fqdn} | cut -d / -f 3 | sort -u > /tmp/gau.tmp"], shell=True)
        f = open(f"/tmp/gau.tmp", "r")
        gau_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm /tmp/gau.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['gau'] = gau_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def crt(args, home_dir, thisFqdn):
    try:
        subprocess.run([f"cd {home_dir}/Tools/tlshelpers; ./getsubdomain {args.fqdn} > /tmp/ctl.tmp"], shell=True)
        f = open(f"/tmp/ctl.tmp", "r")
        ctl_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm /tmp/ctl.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['ctl'] = ctl_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def shosubgo(args, home_dir, thisFqdn):
    try:
        f = open(f"{home_dir}/.keys/.keystore", "r")
        tempArr = f.read().split("\n")
        for line in tempArr:
            temp = line.split(":")
            if temp[0] == "shodan":
                key = temp[1]
        shosubgo_results = subprocess.run([f"{home_dir}/Tools/shosubgo -d {args.fqdn} -s {key}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
        shosubgo_arr = shosubgo_results.stdout.rstrip().split("\n")
        thisFqdn['recon']['subdomains']['shosubgo'] = shosubgo_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def subfinder(args, home_dir, thisFqdn):
    try:
        subprocess.run([f'{home_dir}/go/bin/subfinder -d {args.fqdn} -o /tmp/subfinder.tmp'], shell=True)
        f = open(f"/tmp/subfinder.tmp", "r")
        subfinder_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm -rf /tmp/subfinder.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['subfinder'] = subfinder_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def subfinder_recursive(args, home_dir, thisFqdn):
    try:
        subprocess.run([f'{home_dir}/go/bin/subfinder -d {args.fqdn} -recursive -o /tmp/subfinder.tmp'], shell=True)
        f = open(f"/tmp/subfinder.tmp", "r")
        subfinder_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm -rf /tmp/subfinder.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['subfinder'] = subfinder_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def github_subdomains(args, home_dir, thisFqdn):
    try:
        f = open(f"{home_dir}/.keys/.keystore", "r")
        tempArr = f.read().split("\n")
        for line in tempArr:
            temp = line.split(":")
            if temp[0] == "github":
                key = temp[1]
        github_search_iteration_arr = []
        for x in range(5):
            i = x + 1
            github_search_results = subprocess.run([f"python3 {home_dir}/Tools/github-search/github-subdomains.py -d {args.fqdn} -t {key}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            github_search_arr = github_search_results.stdout.rstrip().split("\n")
            for link in github_search_arr:
                if link not in github_search_iteration_arr:
                    github_search_iteration_arr.append(link)
            print(f"[-] Iteration {i} complete -- {len(github_search_arr)} subdomains found this round!")
        thisFqdn['recon']['subdomains']['githubSearch'] = github_search_iteration_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def gospider(args, home_dir, thisFqdn):
    try:
        subprocess.run([f'cd {home_dir}/go/bin; ./gospider -s "https://{args.fqdn}" -o /tmp/gospider -c 10 -d 1 --other-source --subs --include-subs'], shell=True)
        fqdn = args.fqdn
        outputFile = fqdn.replace(".", "_")
        f = open(f"/tmp/gospider/{outputFile}", "r")
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
        subprocess.run(["rm -rf /tmp/gospider"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['gospider'] = gospider_link_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def gospider_deep(home_dir, thisFqdn):
    try:
        f = open('wordlists/crawl_list.tmp', 'r')
        domain_arr = f.read().rstrip().split("\n")
        for domain in domain_arr:
            subprocess.run([f'cd {home_dir}/go/bin; ./gospider -s "{domain}" -o /tmp/gospider -c 10 -d 1 --other-source --subs --include-subs'], shell=True)
            fqdn = domain.split("/")[2]
            outputFile = fqdn.replace(".", "_")
            f = open(f"/tmp/gospider/{outputFile}", "r")
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
        subprocess.run(["rm -rf /tmp/gospider"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['gospider'] = gospider_link_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def subdomainizer(home_dir, thisFqdn):
    try:
        subprocess.run([f"python3 {home_dir}/Tools/SubDomainizer/SubDomainizer.py -l wordlists/crawl_list.tmp -o /tmp/subdomainizer.tmp -sop /tmp/secrets.tmp"], shell=True)
        f = open("/tmp/subdomainizer.tmp", "r")
        subdomainizer_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm /tmp/subdomainizer.tmp"], stdout=subprocess.DEVNULL, shell=True)
        thisFqdn['recon']['subdomains']['subdomainizer'] = subdomainizer_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def shuffle_dns(args, home_dir, thisFqdn):
    try:
        subprocess.run([f'{home_dir}/go/bin/shuffledns -d {args.fqdn} -w wordlists/all.txt -r wordlists/resolvers.txt -o /tmp/shuffledns.tmp'], shell=True)
        f = open(f"/tmp/shuffledns.tmp", "r")
        shuffledns_arr = f.read().rstrip().split("\n")
        for subdomain in shuffledns_arr:
            if args.fqdn not in subdomain:
                i = shuffledns_arr.index(subdomain)
                del shuffledns_arr[i]
        f.close()
        subprocess.run(["rm -rf /tmp/shuffledns.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['shuffledns'] = shuffledns_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def shuffle_dns_custom(args, home_dir, thisFqdn):
    try:
        subprocess.run([f'{home_dir}/go/bin/shuffledns -d {args.fqdn} -w wordlists/cewl_{args.fqdn}.txt -r wordlists/resolvers.txt -o /tmp/shuffledns_custom.tmp'], shell=True)
        f = open(f"/tmp/shuffledns_custom.tmp", "r")
        shuffledns_custom_arr = f.read().rstrip().split("\n")
        f.close()
        subprocess.run(["rm -rf /tmp/shuffledns_custom.tmp"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        thisFqdn['recon']['subdomains']['shufflednsCustom'] = shuffledns_custom_arr
        update_fqdn_obj(args, thisFqdn)
    except Exception as e:
        print(f"[!] ShuffleDNS w/ Custom Wordlist Failed!\n[!] Exception: {str(e)}")

def consolidate(args):
    thisFqdn = get_fqdn_obj(args)
    consolidated = thisFqdn['recon']['subdomains']['consolidated']
    consolidatedNew = []
    for key in thisFqdn['recon']['subdomains']:
        for subdomain in thisFqdn['recon']['subdomains'][key]:
            if subdomain not in consolidated and args.fqdn in subdomain and "?" not in subdomain:
                consolidated.append(subdomain)
                consolidatedNew.append(subdomain)
    thisFqdn['recon']['subdomains']['consolidated'] = consolidated
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
    f = open("/tmp/consolidated_list.tmp", "w")
    f.write(subdomainStr)
    f.close()
    httprobe_results = subprocess.run([f"cat /tmp/consolidated_list.tmp | {home_dir}/go/bin/httprobe -t 8000 -c 500 -p http:8080 -p http:8000 -p http:8008 -p https:8443 -p https:44300 -p https:44301"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    thisFqdn = r.json()
    httprobe = httprobe_results.stdout.split("\n")
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
    thisFqdn['recon']['subdomains']['httprobe'] = httprobe
    thisFqdn['recon']['subdomains']['httprobeAdded'] = httprobeAdded
    thisFqdn['recon']['subdomains']['httprobeRemoved'] = httprobeRemoved
    update_fqdn_obj(args, thisFqdn)

def build_crawl_list(thisFqdn):
    live_servers = thisFqdn['recon']['subdomains']['httprobe']
    f = open('wordlists/live_servers.tmp', 'w')
    for domain in live_servers:
        f.write(f"{domain}\n")
    f.close()
    subprocess.run([f"ffuf -u 'FUZZ' -fc 403 -w wordlists/live_servers.tmp -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36' -o /tmp/build_crawl_list.tmp"], shell=True)
    with open('/tmp/build_crawl_list.tmp', 'r') as json_file:
        data = json.load(json_file)
    f = open("wordlists/crawl_list.tmp", 'w')
    for result in data['results']:
        subdomain = result['input']['FUZZ']
        print(subdomain)
        try:
            subdomain = subdomain.split("/")[2]
            f.write(f"{subdomain}\n")
        except:
            continue
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
    subprocess.run([f"sudo masscan -p443 --rate 40000 -iL wordlists/aws_ips.txt -oL /tmp/clear_sky_masscan.tmp"], shell=True)
    subprocess.run(["cat /tmp/clear_sky_masscan.tmp | awk {'print $4'} | awk NF | sort -u > /tmp/tls-scan-in.tmp"], shell=True)
    subprocess.run([f"cat /tmp/tls-scan-in.tmp | {home_dir}/Tools/tls-scan/tls-scan --port=443 --concurrency=150 --cacert={home_dir}/Tools/tls-scan/ca-bundle.crt 2>/dev/null -o wordlists/tls-results.json"], shell=True)

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
    requests.post(f'https://hooks.slack.com/services/{token}', json=message_json)

def build_cewl_wordlist(args):
    subprocess.run([f'ls; cewl -d 2 -m 5 -o -a -v -w wordlists/cewl_{args.fqdn}.txt https://{args.fqdn}'], shell=True)

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def get_fqdn_obj(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    return r.json()

def update_fqdn_obj(args, thisFqdn):
    requests.post(f'http://{args.server}:{args.port}/api/auto/update', json=thisFqdn)

def remove_wordlists():
    subprocess.run(["rm wordlists/crawl_*"], shell=True)
    subprocess.run(["rm wordlists/cewl_*"], shell=True)
    subprocess.run(["rm wordlists/live_*"], shell=True)

def get_live_server_text(args, thisFqdn, first):
    print("[!] DEBUG: get_live_server_text method reached.")
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
    f = open('/tmp/populate_burp.tmp', 'w')
    for url in url_list:
        f.write(f'{url}\n')
    f.close()
    subprocess.run([f"ffuf -u 'FUZZ' -w /tmp/populate_burp.tmp -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36' -replay-proxy 'http://{args.proxy}:8080'"], shell=True)
    subprocess.run([f"rm /tmp/populate_burp.tmp"], shell=True)

def check_limit(args):
    thisFqdn = get_fqdn_obj(args)
    unique_domain_count = 0
    for lst in thisFqdn['recon']['subdomains']:
        unique_domain_count += len(thisFqdn['recon']['subdomains'][lst])
    if unique_domain_count > 999:
        print("[!] Unique subdomain limit reached!  Ending the scan for now, but you can always come back and run the scan again without the -l|--limit flat.")
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
        exit()
    else:
        time_left = timeout - now
        print(F"[+] Time remaining before timeout threshold: {time_left}")

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=True)
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=True)
    parser.add_argument('-p','--proxy', help='IP Address of Burp Suite Proxy', required=False)
    parser.add_argument('-d','--fqdn', help='Name of the Root/Seed FQDN', required=True)
    parser.add_argument('-t','--timeout', help='Adds a timeout check after each module (in minutes)', required=False)
    parser.add_argument('--deep', help='Crawl all live servers for subdomains', required=False, action='store_true')
    parser.add_argument('-u', '--update', help='Update AWS IP Certificate Data ( Can Take 48+ Hours! )', required=False, action='store_true')
    parser.add_argument('-l', '--limit', help='Stop the scan when the number of unique subdomains goes above 999', required=False, action='store_true')
    return parser.parse_args()

def main(args):
    starter_timer = Timer()
    print("[-] Running Subdomain Scraping Modules...")
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running Amass against {args.fqdn}")
        amass(args, get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running Sublist3r against {args.fqdn}")
        sublist3r(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running Assetfinder against {args.fqdn}")
        assetfinder(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running Get All URLs against {args.fqdn}")
        gau(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running CRT against {args.fqdn}")
        crt(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running Shosubgo against {args.fqdn}")
        shosubgo(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running Subfinder against {args.fqdn}")
        subfinder(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running Subfinder in Recursive Mode against {args.fqdn}")
        subfinder_recursive(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running Github-Subdomains against {args.fqdn}")
        github_subdomains(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running ShuffleDNS w/ a Default Wordlist against {args.fqdn}")
        shuffle_dns(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running CEWL against {args.fqdn}")
        build_cewl_wordlist(args)
        print(f"[-] Running ShuffleDNS w/ a Custom Wordlist against {args.fqdn}")
        shuffle_dns_custom(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    consolidate(args)
    new_subdomain_length = get_new_subdomain_length(args)
    slack_text = f'The subdomain list for {args.fqdn} has been updated with {new_subdomain_length} new subdomains!'
    # send_slack_notification(get_home_dir(), slack_text)
    try:
        print(f"[-] Running Httprobe against {args.fqdn}")
        httprobe(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    # send_slack_notification(get_home_dir(), get_live_server_text(args, get_fqdn_obj(args), True))
    build_crawl_list(get_fqdn_obj(args))
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    if args.deep:
        print(f"[-] Running DEEP Crawl Scan on {args.fqdn}...")
        try:
            gospider_deep(get_home_dir(), get_fqdn_obj(args))
        except Exception as e:
            print(f"[!] Exception: {e}")
    else:
        try:
            print(f"[-] Running Gospider against {args.fqdn}")
            gospider(args, get_home_dir(), get_fqdn_obj(args))
        except Exception as e:
            print(f"[!] Exception: {e}")
    if args.timeout:
        print("[-] Timeout threshold detected.  Checking timer...")
        check_timeout(args, starter_timer)
    if args.limit:
        print("[-] Unique subdomain limit detected.  Checking count...")
        check_limit(args)
    try:
        print(f"[-] Running Subdomainizer against {args.fqdn}")
        subdomainizer(get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    if not check_clear_sky_data():
        if not args.update:
            print("[!] Clear Sky data not found!  Skipping AWS IP range scan...")
            print("[!] To enable the Clear Sky module, run fire-starter.py in UPDATE MODE (--update)")
        else:
            update_aws_domains()
    print(f"[-] Running Clear-Sky against {args.fqdn}")
    search_data(args, get_fqdn_obj(args))
    consolidate(args)
    new_subdomain_length = get_new_subdomain_length(args)
    slack_text = f'The subdomain list for {args.fqdn} has been updated with {new_subdomain_length} new subdomains!'
    # send_slack_notification(get_home_dir(), slack_text)
    try:
        print(f"[-] Running Httprobe against {args.fqdn}")
        httprobe(args, get_home_dir(), get_fqdn_obj(args))
    except Exception as e:
        print(f"[!] Exception: {e}")
    # send_slack_notification(get_home_dir(), get_live_server_text(args, get_fqdn_obj(args), False))
    populate_burp(args, get_fqdn_obj(args))
    remove_wordlists()
    starter_timer.stop_timer()
    print(f"[+] Done!  Start: {starter_timer.get_start()}  |  Stop: {starter_timer.get_stop()}")

if __name__ == "__main__":
    args = arg_parse()
    main(args)