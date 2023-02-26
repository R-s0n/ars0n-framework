import requests, argparse, subprocess, sys, json, math, threading
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

extension_blacklist = [".pdf", ".jpg", ".png", ".svg"]

def get_links(fqdn, url, links):
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    a_tags = soup.find_all('a')
    for tag in a_tags:
        if tag.get('href') != None:
            tag_to_add = tag.get('href')
            if ".pdf" in tag_to_add or ".jpg" in tag_to_add or ".png" in tag_to_add or ".svg" in tag_to_add or "mailto:" in tag_to_add:
                continue
            if "?" in tag_to_add:
                tag_to_add = tag_to_add.split("?")[0]
            if "#" in tag_to_add:
                tag_to_add = tag_to_add.split("#")[0]
            if tag_to_add[:4] == "http":
                if tag_to_add[:len(url)] == url:
                    if tag_to_add not in links:
                        links.append(tag_to_add)
            elif tag_to_add[:1] == "/":
                tag_to_add = f"{fqdn}{tag_to_add}"
                if tag_to_add not in links:
                    links.append(tag_to_add)
            else:
                tag_to_add = f"{fqdn}/{tag_to_add}"
                if tag_to_add not in links:
                    links.append(tag_to_add)
    return links

def get_scripts(url, script_links):
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    script_tags = soup.find_all('script')
    for tag in script_tags:
        if tag.get('src') != None:
            tag_to_add = tag.get('src')
            if "?" in tag_to_add:
                tag_to_add = tag_to_add.split("?")[0]
            if tag_to_add[:4] == "http":
                if tag_to_add not in script_links:
                    script_links.append(tag_to_add)
            elif tag_to_add[:1] == "/":
                tag_to_add = f"{url}{tag_to_add}"
                if tag_to_add not in script_links:
                    script_links.append(f"{tag_to_add}")
            else:
                tag_to_add = f"{url}/{tag_to_add}"
                if tag_to_add not in script_links:
                    script_links.append(f"{tag_to_add}")
    return script_links

def crawl_links(fqdn, depth, links):
    if depth == "full":
        while True:
            num_of_links = len(links)
            temp = links
            for link in temp:
                if ".pdf" in link or ".jpg" in link or ".png" in link or ".svg" in link or "mailto:" in link:
                    links.remove(link)
                    continue
                else:
                    links = get_links(fqdn, link, links)
            if len(links) == num_of_links:
                return links
    else:
        counter = 1
        while True:
            num_of_links = len(links)
            temp = links
            for link in temp:
                if ".pdf" in link or ".jpg" in link or ".png" in link or ".svg" in link or "mailto:" in link:
                    links.remove(link)
                    continue
                else:
                    links = get_links(fqdn, link, links)
            if len(links) == num_of_links or counter >= int(depth) or len(links) > 99:
                return links
            counter += 1

def clean_urls(url_list):
    clean_url_list = []
    for url in url_list:
        if "?" in url:
            url_split = url.split("?")
            if url_split[0] not in clean_url_list:
                clean_url_list.append(url_split[0])
        else:
            if url not in clean_url_list:
                clean_url_list.append(url)
    return clean_url_list

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def send_slack_notification(args, url, package):
    home_dir = get_home_dir()
    message_json = {'text':f'Package {package} was found running on {url}!  (This will have a lot more information after I add this to the framework...)','username':'Vuln Disco Box','icon_emoji':':dart:'}
    f = open(f'{home_dir}/.keys/slack_web_hook')
    token = f.read()
    slack_auto = requests.post(f'https://hooks.slack.com/services/{token}', json=message_json)

def wappalyzer(url):
    wappalyzer = subprocess.run([f'wappalyzer {url} -p'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return wappalyzer.stdout

def npm_package_scan(args, url_list):
    packages = []
    cves = requests.post(f"http://{args.server}:{args.port}/api/cve/all")
    cve_json = json.loads(cves.text)
    for cve in cve_json:
        if cve['javascript'] is True:
            packages.append(cve['searchTerm'])
            blacklist = cve['blacklistTerms']
    for url in url_list:
        script_links = []
        raw_scripts = []
        links = []
        if "http" in url:
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            remaining = len(url_list) - url_list.index(url)
            print(f"[-] Scanning {url} -- Time: {time} -- URLs Remaining: {remaining}")
            if int(args.depth) > 0:
                links = get_links(url, url, links)
                if int(args.depth) > 1:
                    links = crawl_links(url, args.depth, links)
            wappalyzer_string = wappalyzer(url)
            wappalyzer_json = json.loads(wappalyzer_string)
            for package in packages:
                if package.lower() in wappalyzer_string:
                    for term in blacklist:
                        if term not in wappalyzer_string:
                            print(f"[+] Package {package} was found on {url}! (From Wappalyzer)")
                            send_slack_notification(args, url, package)
                            print(json.dumps(wappalyzer_json, indent=4))
                            continue
            links.append(url)
            for link in links:
                script_links = get_scripts(link, script_links)
            for script in script_links:
                for package in packages:
                    if package.lower() in script.lower():
                        for term in blacklist:
                            if term not in wappalyzer_string:
                                print(f"[+] Package {package} was found on {url}! (From Script Scan)")
                                send_slack_notification(args, url, package)
                                print(json.dumps(wappalyzer_json, indent=4))
        else:
            print("[!] Invalid URL!  Skipping...")


def get_fqdns(args):
    res = requests.post(f'http://{args.server}:{args.port}/api/auto', data={"fqdn":args.domain})
    fqdn_json = res.json()
    fqdn_list = fqdn_json['recon']['subdomains']['httprobe']
    return fqdn_list


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=True)
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=True)
    parser.add_argument('-D','--domain', help='FQDN of Root/Seed Being Targeted', required=True)
    parser.add_argument('-d','--depth', help='Depth of Crawl ( Default is 0 )', nargs='?', default="0", required=False)
    parser.add_argument('-j','--js', help='Scan For JavaScript Package', required=False, action='store_true')
    return parser.parse_args()

def main(args):
    if args.js is False:
        print("[!] Please select atleast one scanning type ( -j/--js | )")
        sys.exit(2)
    fqdn_list = get_fqdns(args)
    clean_url_list = clean_urls(fqdn_list)
    npm_package_scan(args, clean_url_list)
    print("[+] Done!")

if __name__ == "__main__":
    args = arg_parse()
    main(args)