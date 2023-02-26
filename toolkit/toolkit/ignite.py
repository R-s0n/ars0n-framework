import requests, sys, subprocess, json, time, math, random, argparse, string
import xmltodict
from javasoup import get_soup
from datetime import datetime
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def wordlist_scan(args, target_url_string, blacklist=[], filter_regex="404 Not Found", wordlist="start.txt"):
    home_dir = get_home_dir()
    thisUrl = get_target_url_object(args, target_url_string)
    print(filter_regex)
    subprocess.run([f"{home_dir}/go/bin/ffuf -w 'wordlists/{wordlist}' -u {target_url_string}/FUZZ -H 'Te: trailers' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' -recursion -recursion-depth 4 -timeout 3 -r -p 0.1-3.0 -sa -t 50 -fr '{filter_regex}' -fc 403,401 -replay-proxy http://{args.proxy}:8080 -o temp/ffuf-results.tmp -of json"], shell=True)
    with open('temp/ffuf-results.tmp') as json_file:
        data = json.load(json_file)
    for result in data['results']:
        try:
            if result['input']['FUZZ'][-1] == "/":
                result_data = {"endpoint":result['input']['FUZZ'][:-1], "statusCode":result['status'], "responseLength":result['length']}
            else:
                result_data = {"endpoint":result['input']['FUZZ'], "statusCode":result['status'], "responseLength":result['length']}
        except Exception as e:
            # print(f"[!] EXCEPTION: {e}")
            continue
        if len(result_data['endpoint']) < 1:
            result_data['endpoint'] = "/"
        if result_data['endpoint'][0] != "/":
            result_data['endpoint'] = f"/{result_data['endpoint']}"
        if '?' in result_data['endpoint']:
            temp = result_data['endpoint'].split('?')
            result_data['endpoint'] = temp[0]
        if '#' in result_data['endpoint']:
            temp = result_data['endpoint'].split('#')
            result_data['endpoint'] = temp[0]
        result_str = result_data['endpoint']
        current_endpoints_list = []
        current_endpoints = thisUrl['endpoints']
        for endpoint in current_endpoints:
            current_endpoints_list.append(endpoint['endpoint'])
        if result_str not in current_endpoints_list or ".png" not in result_str or ".PNG" not in result_str or ".jpg" not in result_str or ".JPG" not in result_str:
            thisUrl['endpoints'].append(result_data)
    update_url(args, thisUrl)

def wordlist_scan_files(args, target_url_string, blacklist=[], filter_regex="404 Not Found"):
    thisUrl = get_target_url_object(args, target_url_string)
    endpoint_list = []
    endpoints = thisUrl['endpoints']
    for endpoint in endpoints:
        endpoint_list.append(endpoint['endpoint'])
    home_dir = get_home_dir()
    for endpoint in endpoint_list:
        skip = False
        for blacklisted_endpoint in blacklist:
            if blacklisted_endpoint == endpoint:
                skip = True
        if skip == True:
            continue
        if "." in endpoint[-6:] and ".com" not in endpoint[-6:]:
            print("Skipping File...")
            print(endpoint)
            continue
        subprocess.run([f"{home_dir}/go/bin/ffuf -w 'wordlists/files.txt' -u {target_url_string}{endpoint}/FUZZ -H 'Te: trailers' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' -recursion -recursion-depth 4 -timeout 3 -r -p 0.1-3.0 -sa -t 50 -fr '{filter_regex}' -fc 403,401 -replay-proxy http://{args.proxy}:8080 -o temp/ffuf-results.tmp -of json"], shell=True)
        with open('temp/ffuf-results.tmp') as json_file:
            data = json.load(json_file)
        for result in data['results']:
            if result['input']['FUZZ'][-1] == "/":
                result_data = {"endpoint":result['input']['FUZZ'][:-1], "statusCode":result['status'], "responseLength":result['length']}
            else:
                result_data = {"endpoint":result['input']['FUZZ'], "statusCode":result['status'], "responseLength":result['length']}
            if len(result_data['endpoint']) < 1:
                result_data['endpoint'] = "/"
            if result_data['endpoint'][0] != "/":
                result_data['endpoint'] = f"/{result_data['endpoint']}"
            result_str = result_data['endpoint']
            current_endpoints_list = []
            current_endpoints = thisUrl['endpoints']
            for endpoint in current_endpoints:
                current_endpoints_list.append(endpoint['endpoint'])
            if '?' in result_data['endpoint']:
                temp = result_data['endpoint'].split('?')
                result_data['endpoint'] = temp[0]
            if '#' in result_data['endpoint']:
                temp = result_data['endpoint'].split('#')
                result_data['endpoint'] = temp[0]
            if result_str not in current_endpoints_list or ".png" not in result_str or ".PNG" not in result_str or ".jpg" not in result_str or ".JPG" not in result_str:
                thisUrl['endpoints'].append(result_data)
        wordlist_len = len(thisUrl['completedWordlists'])
        update_url(args, thisUrl)

def crawl_scan(args, target_url_string, blacklist=[], filter_regex="404 Not Found"):
    thisUrl = get_target_url_object(args, target_url_string)
    url_list = [f"{target_url_string}"]
    for endpoint in thisUrl['endpoints']:
        url_list.append(f"{target_url_string}{endpoint['endpoint']}")
    print("url_list: ")
    print(url_list)
    for url in url_list:
        print(f"Testing {url}")
        length = len(target_url_string) + 1
        prefix = url[length:]
        print(f"Prefix: {prefix}")
        skip = False
        for blacklisted_endpoint in blacklist:
            if f"{target_url_string}{blacklisted_endpoint}" == url:
                skip = True
                print(f"[!] Endpoint {blacklisted_endpoint} is blacklisted.")
        if skip == True:
            print("[!] Skipping blacklisted endpoint...")
            continue
        if "." in url[-6:] and ".com" not in url[-6:] and ".org" not in url[-6:] and ".gov" not in url[-6:]:
            print(f"[!] Skipping File {url}...")
            continue
        res = requests.get(url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.findAll('a')
        javasoup = BeautifulSoup(get_soup(url), 'html.parser')
        js_links = javasoup.findAll('a')
        soup_scripts = soup.findAll('script')
        javasoup_scripts = javasoup.findAll('script')
        for script in javasoup_scripts:
            if script not in soup_scripts:
                soup_scripts.append(script)
        print("Links:")
        print(links)
        print("JS Links:")
        print(js_links)
        print("Scripts:")
        print(soup_scripts)
        check_scripts(args, target_url_string, soup_scripts)
        for link in js_links:
            if link not in links:
                links.append(link)
        for link in links:
            try:
                try:
                    href = link['href']
                except:
                    href = link['src']
            except Exception as e:
                continue
            if "http" in href:
                if target_url_string in href:
                    url_length = len(target_url_string)
                    path = href[url_length:].split("/")
                    path_list = []
                    for p in path:
                        if len(p) < 1:
                            path.remove(p)
                        else:
                            print(p)
                            result_data = {"endpoint":p, "statusCode":000, "responseLength":000}
                            current_endpoints_list = []
                            current_endpoints = thisUrl['endpoints']
                            for endpoint in current_endpoints:
                                current_endpoints_list.append(endpoint['endpoint'])
                            if p not in current_endpoints_list:
                                thisUrl['endpoints'].append(result_data)
            else:
                print(href)
                try:
                    if href[0] == "/":
                        result_data = {"endpoint":href, "statusCode":000, "responseLength":000}
                    else:
                        result_data = {"endpoint":f"/{href}", "statusCode":000, "responseLength":000}
                except Exception as e:
                    # print(e)
                    continue
                current_endpoints_list = []
                current_endpoints = thisUrl['endpoints']
                for endpoint in current_endpoints:
                    current_endpoints_list.append(endpoint['endpoint'])
                if href not in current_endpoints_list:
                    thisUrl['endpoints'].append(result_data)
        write_wordlist(args, thisUrl)
        home_dir = get_home_dir()
        subprocess.run([f"{home_dir}/go/bin/ffuf -w 'wordlists/crawl_wordlist_{args.domain}.txt' -u {url}FUZZ -recursion -recursion-depth 4 -r -p 0.1-3.0 -sa -t 50 -fr '{filter_regex}' -fc 403,401 -replay-proxy http://{args.proxy}:8080 -o temp/ffuf-results.tmp -of json"], shell=True)
        thisUrl = get_target_url_object(args, target_url_string)
        with open('temp/ffuf-results.tmp') as json_file:
            data = json.load(json_file)
        for result in data['results']:
            try:
                if result['input']['FUZZ'][-1] == "/":
                    result_data = {"endpoint":prefix + result['input']['FUZZ'][:-1], "statusCode":result['status'], "responseLength":result['length']}
                else:
                    result_data = {"endpoint":prefix + result['input']['FUZZ'], "statusCode":result['status'], "responseLength":result['length']}
            except:
                continue
            print(result_data['endpoint'])
            if len(result_data['endpoint']) < 1:
                result_data['endpoint'] = "/"
            if result_data['endpoint'][0] != "/":
                result_data['endpoint'] = f"/{result_data['endpoint']}"
            if '?' in result_data['endpoint']:
                temp = result_data['endpoint'].split('?')
                result_data['endpoint'] = temp[0]
            if '#' in result_data['endpoint']:
                temp = result_data['endpoint'].split('#')
                result_data['endpoint'] = temp[0]
            result_str = result_data['endpoint']
            current_endpoints_list = []
            current_endpoints = thisUrl['endpoints']
            for endpoint in current_endpoints:
                current_endpoints_list.append(endpoint['endpoint'])
            if result_str not in current_endpoints_list and ".png" not in result_str and ".PNG" not in result_str and ".jpg" not in result_str and ".JPG" not in result_str:
                thisUrl['endpoints'].append(result_data)
        update_url(args, thisUrl)

def remove_duplicates(args, target_url_string):
    thisUrl = get_target_url_object(args, target_url_string)
    endpoints = []
    new_url_endpoints = []
    for endpoint in thisUrl['endpoints']:
        try:
            if endpoint['endpoint'][-1] == "/":
                endpoint['endpoint'] = endpoint['endpoint'][:-1]
            if endpoint['endpoint'] in endpoints:
                continue
            else:
                new_url_endpoints.append(endpoint)
                endpoints.append(endpoint['endpoint'])
        except Exception as e:
            # print(e)
            continue
    thisUrl['endpoints'] = new_url_endpoints
    update_url(args, thisUrl)
    
def random_string(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def write_xml_file(url):
    res = requests.get(url, verify=False)
    with open('temp/xml.tmp', 'wb') as f:
        f.write(res.content)
    f.close()

def check_scripts(args, target_url_string, scripts):
    thisUrl = get_target_url_object(args, target_url_string)
    for script in scripts:
        print(script)
        print(type(script))
        try:
            source = script['src']
        except Exception as e:
            # print(e)
            continue
        print(f"{target_url_string}{source}")
        try:
            res = requests.get(f"{target_url_string}{source}", verify=False)
            if res.status_code == 200:
                result_data = {"endpoint":script['src'], "statusCode":200, "responseLength":000}
                thisUrl['endpoints'].append(result_data)
        except Exception as e:
            print(e)
            continue
    update_url(args, thisUrl)

def check_xml_sitemap(args, target_url_string, filter_regex, sitemap_endpoint="/sitemap.xml"):
    res = requests.get(f"{target_url_string}{sitemap_endpoint}", verify=False)
    if res.status_code == 200:
        print("[+] Found sitemap.xml!")
        thisUrl = get_target_url_object(args, target_url_string)
        url = f"{target_url_string}/sitemap.xml"
        write_xml_file(url)
        with open("temp/xml.tmp") as xml_file:
            try:
                data_dict = xmltodict.parse(xml_file.read())
                xml_file.close()
                sitemap_string = json.dumps(data_dict)
                sitemap_json = json.loads(sitemap_string)
                url_list = []
                length = len(target_url_string)
                f = open(f"wordlists/sitemap_{args.domain}", 'w')
                for location in sitemap_json['urlset']['url']:
                    endpoint = location['loc'][length:]
                    f.write(f"{endpoint}\n")
                f.close()
                home_dir = get_home_dir()
                subprocess.run([f"{home_dir}/go/bin/ffuf -w 'wordlists/sitemap_{args.domain}' -u {target_url_string}FUZZ -H 'Te: trailers' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' -recursion -recursion-depth 4 -r -p 0.1-3.0 -sa -t 50 -fr '{filter_regex}' -fc 403,401 -replay-proxy http://{args.proxy}:8080 -o temp/ffuf-results.tmp -of json"], shell=True)
                with open('temp/ffuf-results.tmp') as json_file:
                    data = json.load(json_file)
                for result in data['results']:
                    result_data = {"endpoint":result['input']['FUZZ'], "statusCode":result['status'], "responseLength":result['length']}
                    if len(result_data['endpoint']) < 1:
                        result_data['endpoint'] = "/"
                    if result_data['endpoint'][0] != "/":
                        result_data['endpoint'] = f"/{result_data['endpoint']}"
                    result_str = result_data['endpoint']
                    current_endpoints_list = []
                    current_endpoints = thisUrl['endpoints']
                    for endpoint in current_endpoints:
                        current_endpoints_list.append(endpoint['endpoint'])
                    if '?' in result_data['endpoint']:
                        temp = result_data['endpoint'].split('?')
                        result_data['endpoint'] = temp[0]
                    if '#' in result_data['endpoint']:
                        temp = result_data['endpoint'].split('#')
                        result_data['endpoint'] = temp[0]
                    if result_str not in current_endpoints_list:
                        thisUrl['endpoints'].append(result_data)
                update_url(args, thisUrl)
            except Exception as e:
                # print(e)
                print("[!] Failed to load sitemap.xml!  Skipping...")
        subprocess.run(['rm wordlists/sitemap_*'], shell=True)
        
            

def check_robots(args, target_url_string):
    res = requests.get(f"{target_url_string}/robots.txt", verify=False)
    if res.status_code == 200:
        print("[+] Found Robots.txt!")
        robots = res.text
        robots_list = robots.split("\n")
        endpoints = []
        for robot in robots_list:
            if "Disallow" in robot:
                temp_endpoint = robot.split(":")[1]
                temp_endpoint = temp_endpoint.replace(" /", "/")
                if len(temp_endpoint) < 3:
                    temp_endpoint = temp_endpoint.replace("/*", "")
                length = len(temp_endpoint)
                if temp_endpoint[length-1:] == "/":
                    temp_endpoint = temp_endpoint[:length-1]
                endpoints.append(temp_endpoint)
        thisUrl = get_target_url_object(args, target_url_string)
        for endpoint in endpoints:
            try:
                res_two = requests.get(f'{target_url_string}{endpoint}', verify=False)
                if res_two.status_code < 400:
                    result_data = {"endpoint":endpoint, "statusCode":res_two.status_code, "responseLength":000}
                    thisUrl['endpoints'].append(result_data)
            except Exception as e:
                print(f"[!] Something went wrong when accessing {target_url_string}{endpoint}!  Skipping...")
        update_url(args, thisUrl)


def check_thisdoesnotexist(args, target_url_string):
    rand_string = random_string()
    res = requests.get(f"{target_url_string}/{rand_string}", verify=False)
    if res.status_code != 404:
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            if soup.title != None:
                return soup.title
        except Exception as e:
            return res.text
    return "404 Not Found"

def check_dynamic_routing(args, target_url_string):
    thisUrl = get_target_url_object(args, target_url_string)
    endpoint_list = []
    for endpoint in thisUrl['endpoints']:
        endpoint_list.append(endpoint['endpoint'])
    rand_string = random_string()
    blacklist = []
    for endpoint in endpoint_list:
        try:
            res = requests.get(f"{target_url_string}{endpoint}/{rand_string}", verify=False)
            if res.status_code == 200:
                print(f"[!] {endpoint} appears to be dynamic.  Adding to blacklist...")
                blacklist.append(endpoint)
        except Exception as e:
            # print(e)
            blacklist.append(endpoint)
    return blacklist

def final_status_check(args, target_url_string):
    thisUrl = get_target_url_object(args, target_url_string)
    endpoints = []
    new_url_endpoints = []
    for endpoint in thisUrl['endpoints']:
        try:
            endpoint_string = endpoint['endpoint']
            res = requests.get(f"{target_url_string}{endpoint_string}", verify=False)
            if res.status_code != 404:
                new_url_endpoints.append(endpoint)
        except Exception as e:
            # print(e)
            continue
    thisUrl['endpoints'] = new_url_endpoints
    update_url(args, thisUrl)

def write_wordlist(args, thisUrl):
    f = open(f'wordlists/crawl_wordlist_{args.domain}.txt', 'w')
    for endpoint in thisUrl['endpoints']:
        f.write(f"{endpoint['endpoint']}\n")
    f.close()

def delete_wordlists():
    subprocess.run(["rm wordlists/crawl_wordlist_*; rm temp/*"], shell=True)

def update_url(args, thisUrl):
    res = requests.post(f'http://{args.server}:{args.port}/api/url/auto/update', json=thisUrl, headers={'Content-type':'application/json'}, proxies={'http':f'http://{args.proxy}:8080'})

def get_target_url_object(args, target_url_string):
    r = requests.post(f'http://{args.server}:{args.port}/api/url/auto', data={'url':target_url_string})
    return r.json()

def get_target_url_string(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.domain})
    thisFqdn = r.json()
    return thisFqdn['targetUrls'][0]

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--domain', help='FQDN of Target URL', required=True)
    parser.add_argument('-p','--port', help='Port of MongoDB API', required=True)
    parser.add_argument('-s','--server', help='IP Address of MongoDB API', required=True)
    parser.add_argument('-P','--proxy', help='IP Address of Burp Suite Proxy', required=False)
    return parser.parse_args()

def main(args):
    # ToDo:
    # 1. Fix hash fragment issue
    # 1. compensate for
    # javascript:go('client1.php')
    # javascript:go('client2.php')
    # javascript:go('client3.php')
    # javascript:go('wsdlclient1.php')
    # javascript:go('wsdlclient2.php')
    # javascript:go('wsdlclient3.php?method=function')
    # javascript:go('wsdlclient3.php?method=instance')
    # javascript:go('wsdlclient3.php?method=class')
    # javascript:go('wsdlclient5.php')
    # javascript:go('wsdlclient6.php')
    # javascript:go('wsdlclient7.php')
    # javascript:go('wsdlclient8.php')
    # javascript:go('wsdlclient9.php')
    # javascript:go('wsdlclient12.php?method=ItemSearch2')
    # javascript:go('wsdlclient12.php?method=ListSearch')
    # javascript:go('wsdlclient12.php?method=CartCreate')
    # javascript:go('wsdlclient13.php')
    # javascript:go('wsdlclient14.php')
    # javascript:go('getfile1client.php')
    # javascript:go('getfile2client.php')
    target_url_string = get_target_url_string(args)
    print(f"[-] Enumerating endpoints on {target_url_string}")
    print("[-] Checking for custom 404 page...")
    filter_regex = check_thisdoesnotexist(args, target_url_string)
    if filter_regex == "404 Not Found":
        print("[+] Custom 404 page was NOT detected.  Continuing...")
    else:
        print("[!] Custom 404 page detected!  Adding REGEX filter...")
    print("[-] Checking for Robots.txt file...")
    check_robots(args, target_url_string)
    print("[-] Checking for sitemap.xml file...")
    check_xml_sitemap(args, target_url_string, filter_regex)
    print("[-] Performing initial wordlist scan...")
    blacklist = []
    wordlist_scan(args, target_url_string, blacklist, filter_regex)
    print("[-] Checking for endpoints with dynamic routing...")
    blacklist = check_dynamic_routing(args, target_url_string)
    print("[-] Performing crawl scan...")
    crawl_scan(args, target_url_string, blacklist, filter_regex)
    print("[-] Cleaning up the data...")
    remove_duplicates(args, target_url_string)
    print("[-] Performing deeper wordlist scan...")
    print("[-] Checking for endpoints with dynamic routing...")
    blacklist = check_dynamic_routing(args, target_url_string)
    wordlist = "deep.txt"
    wordlist_scan(args, target_url_string, blacklist, filter_regex, wordlist)
    print("[-] Checking for endpoints with dynamic routing...")
    blacklist = check_dynamic_routing(args, target_url_string)
    print("[-] Performing crawl scan...")
    crawl_scan(args, target_url_string, blacklist, filter_regex)
    print("[-] Cleaning up the data...")
    remove_duplicates(args, target_url_string)
    print("[-] Checking for endpoints with dynamic routing...")
    blacklist = check_dynamic_routing(args, target_url_string)
    print("[-] Performing file scan on all endpoints...")
    wordlist_scan_files(args, target_url_string, blacklist, filter_regex)
    print("[-] Checking for endpoints with dynamic routing...")
    blacklist = check_dynamic_routing(args, target_url_string)
    print("[-] Cleaning up the data...")
    remove_duplicates(args, target_url_string)
    print("[-] Performing crawl scan...")
    crawl_scan(args, target_url_string, blacklist, filter_regex)
    print("[-] Checking for endpoints with dynamic routing...")
    blacklist = check_dynamic_routing(args, target_url_string)
    print("[-] Cleaning up the data...")
    remove_duplicates(args, target_url_string)  
    # Add javascript crawl using javasoup
    crawl_scan(args, target_url_string, blacklist, filter_regex)
    print("[-] Performing final cleanup...")
    remove_duplicates(args, target_url_string)
    delete_wordlists()
    final_status_check(args, target_url_string)
    print(f"[+] Ignite.py completed successfully!")

if __name__ == "__main__":
    args = arg_parse()
    main(args)