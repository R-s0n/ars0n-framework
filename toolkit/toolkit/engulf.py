# Automated Parameter Discovery

import requests, sys, subprocess, argparse, json, time, math, random
from datetime import datetime

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def get_target_url_string(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.domain})
    thisFqdn = r.json()
    return thisFqdn['targetUrls'][0]

def get_target_url_object(args, target_url_string):
    res = requests.post(f'http://{args.server}:{args.port}/api/url/auto', data={'url':target_url_string})
    return res.json()

def get_endpoints_from_url_object(thisUrl):
    endpoints = thisUrl['endpoints']
    return sorted(endpoints, key=lambda k: k['statusCode'])

def get_number_of_endpoints(endpoints):
    counter = 0
    for endpoint in endpoints:
        if str(endpoint['statusCode'])[0] == '2':
            counter += 1
    print(f"[-] Starting parameter enumeration on {thisUrl['url']}")
    print(f"[-] {counter} parameters found with a 2XX response code")

def run_arjun_get(args, sorted_endpoints, url):
    for endpoint in sorted_endpoints:
        if str(endpoint['statusCode'])[0] == '2' and len(endpoint['arjun']['params']) < 1:
            print(f"[-] Target Endpoint: {endpoint['endpoint']}\n[-] Status: {endpoint['statusCode']} -- Length: {endpoint['responseLength']}")
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            print("Start Time:", time)
            try:
                thisEndpoint = endpoint['endpoint']
                if thisEndpoint[-4:] == ".ico" or thisEndpoint[-4:] == ".txt":
                    print(f"[!] Endpoint is a static file.  Skipping...")
                    continue
            except:
                print("[-] Targeting root directory...")
                thisEndpoint = "/"
            target = url + thisEndpoint
            print(f"[-] Scanning {target} for hidden parameters...")
            subprocess.run([f"arjun -u {target}  -oJ temp/arjun-test.tmp -oT arjun-text.txt -w wordlists/params.txt -oB {args.proxy}:8080"], shell=True)
            with open('temp/arjun-test.tmp') as json_file:
                data = json.load(json_file)
            print(f"[+] Scan complete!")
            if target not in data:
                print(f"[!] No parameters found for {target} -- Skipping database update...")
                continue
            for param in data[target]['params']:
                print(f'[+] Parameter found: {param}')
            print(f"[-] Updating database...")
            try:
                r = requests.post(f'http://{args.server}:{args.port}/api/url/auto', data={'url':url})
                updateUrl = r.json()
                for endpoint in updateUrl['endpoints']:
                    if endpoint['endpoint'] == thisEndpoint:
                        endpointToUpdate = endpoint
                        endpointIndex = updateUrl['endpoints'].index(endpoint)
                updateUrl['endpoints'][endpointIndex]['arjun'] = {"method": data[target]['method'], "params": data[target]['params']}
                requests.post(f'http://{args.server}:{args.port}/api/url/auto/update', json=updateUrl)
            except Exception as e:
                print(f"[!] Database updated failed.  ")
                print(f"[!] {e}")

def run_arjun_post(args, sorted_endpoints, url):
    for endpoint in sorted_endpoints:
        if str(endpoint['statusCode'])[0] == '2' and len(endpoint['arjunPost']['params']) < 1:
            print(f"[-] Target Endpoint: {endpoint['endpoint']}\n[-] Status: {endpoint['statusCode']} -- Length: {endpoint['responseLength']}")
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            print("Start Time:", time)
            try:
                thisEndpoint = endpoint['endpoint']
                if thisEndpoint[-4:] == ".ico" or thisEndpoint[-4:] == ".txt":
                    print(f"[!] Endpoint is a static file.  Skipping...")
                    continue
            except:
                print("[-] Targeting root directory...")
                thisEndpoint = "/"
            target = url + thisEndpoint
            print(f"[-] Scanning {target} for hidden parameters...")
            subprocess.run([f"arjun -u {target}  -oJ temp/arjun-test.tmp -oT arjun-text.txt -w wordlists/params.txt -oB {args.proxy}:8080 -q -m POST"], shell=True)
            with open('temp/arjun-test.tmp') as json_file:
                data = json.load(json_file)
            print(f"[+] Scan complete!")
            if target not in data:
                print(f"[!] No parameters found for {target} -- Skipping database update...")
                continue
            for param in data[target]['params']:
                print(f'[+] Parameter found: {param}')
            print(f"[-] Updating database...")
            try:
                r = requests.post(f'http://{args.server}:{args.port}/api/url/auto', data={'url':url})
                updateUrl = r.json()
                for endpoint in updateUrl['endpoints']:
                    if endpoint['endpoint'] == thisEndpoint:
                        endpointToUpdate = endpoint
                        endpointIndex = updateUrl['endpoints'].index(endpoint)
                updateUrl['endpoints'][endpointIndex]['arjunPost'] = {"method": data[target]['method'], "params": data[target]['params']}
                requests.post(f'http://{args.server}:{args.port}/api/url/auto/update', json=updateUrl)
            except Exception as e:
                print(f"[!] Database updated failed.  ")
                print(f"[!] {e}")

def run_arjun_json(args, sorted_endpoints, url):
    for endpoint in sorted_endpoints:
        if str(endpoint['statusCode'])[0] == '2' and len(endpoint['arjunJson']['params']) < 1:
            print(f"[-] Target Endpoint: {endpoint['endpoint']}\n[-] Status: {endpoint['statusCode']} -- Length: {endpoint['responseLength']}")
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            print("Start Time:", time)
            try:
                thisEndpoint = endpoint['endpoint']
                if thisEndpoint[-4:] == ".ico" or thisEndpoint[-4:] == ".txt":
                    print(f"[!] Endpoint is a static file.  Skipping...")
                    continue
            except:
                print("[-] Targeting root directory...")
                thisEndpoint = "/"
            target = url + thisEndpoint
            print(f"[-] Scanning {target} for hidden parameters...")
            subprocess.run([f"arjun -u {target}  -oJ temp/arjun-test.tmp -oT arjun-text.txt -w wordlists/params.txt -oB {args.proxy}:8080 -q -m JSON"], shell=True)
            with open('temp/arjun-test.tmp') as json_file:
                data = json.load(json_file)
            print(f"[+] Scan complete!")
            if target not in data:
                print(f"[!] No parameters found for {target} -- Skipping database update...")
                continue
            for param in data[target]['params']:
                print(f'[+] Parameter found: {param}')
            print(f"[-] Updating database...")
            try:
                r = requests.post(f'http://{args.server}:{args.port}/api/url/auto', data={'url':url})
                updateUrl = r.json()
                for endpoint in updateUrl['endpoints']:
                    if endpoint['endpoint'] == thisEndpoint:
                        endpointToUpdate = endpoint
                        endpointIndex = updateUrl['endpoints'].index(endpoint)
                updateUrl['endpoints'][endpointIndex]['arjunJson'] = {"method": data[target]['method'], "params": data[target]['params']}
                requests.post(f'http://{args.server}:{args.port}/api/url/auto/update', json=updateUrl)
            except Exception as e:
                print(f"[!] Database updated failed.  ")
                print(f"[!] {e}")

def main(args):
    target_url_string = get_target_url_string(args)
    thisUrl = get_target_url_object(args, target_url_string)
    endpoints = get_endpoints_from_url_object(thisUrl)
    run_arjun_get(args, endpoints, target_url_string)
    run_arjun_post(args, endpoints, target_url_string)
    run_arjun_json(args, endpoints, target_url_string)
    print("[+] Done!")

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--domain', help='FQDN of Target URL', required=True)
    parser.add_argument('-p','--port', help='Port of MongoDB API', required=True)
    parser.add_argument('-s','--server', help='IP Address of MongoDB API', required=True)
    parser.add_argument('-P','--proxy', help='IP Address of Burp Suite Proxy', required=False)
    return parser.parse_args()

if __name__ == "__main__":
    args = arg_parse()
    main(args)