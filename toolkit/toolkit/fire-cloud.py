import requests
import argparse
import re
import xml.etree.ElementTree as ET
import subprocess
from datetime import datetime

class Logger:
    def __init__(self):
        subprocess.run(["[ -f ../logs/log.txt ] || touch logs/log.txt"], shell=True)
        with open("../logs/log.txt", "r") as file:
            self.init_log_data = file.readlines()
            self.init_log_len = len(self.init_log_data)
        with open("../logs/log.txt", "a") as file:
            log_start_time = datetime.now()
            flag = "[INIT]"
            running_script = "Fire-Cloud.py"
            message = "Logger Initialized"
            file.write(f"{flag} {log_start_time} | {running_script} -- {message}\n")

    def write_to_log(self, flag, running_script, message):
        with open("../logs/log.txt", "a") as file:
            log_start_time = datetime.now()
            file.write(f"{flag} {log_start_time} | {running_script} -- {message}\n")
        with open("../logs/temp_log.txt", "a") as file:
            log_start_time = str(datetime.now())
            file.write(f"{flag} {log_start_time} | {running_script} -- {message}\n")

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def update_fqdn_obj(args, thisFqdn):
    res = requests.post(f'http://{args.server}:{args.port}/api/auto/update', json=thisFqdn)

def aws_access_key_check(logger):
    home_dir = get_home_dir()
    print(f"[+] Checking for AWS Credentials in {home_dir}/.aws/credentials")
    try:
        cred_check = subprocess.run(["ls", f"{home_dir}/.aws/credentials"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if cred_check.returncode == 0:
            print("[+] AWS Credentials found!")
            logger.write_to_log("[MSG]","Fire-Cloud.py",f"AWS Credentials Provided.  Continuing Scan...")
            return True
        else:
            print("[-] AWS Credentials not found, add them by running aws configure for maximum effectiveness.")
            print("\n")
            logger.write_to_log("[WARN]","Fire-Cloud.py",f"AWS Credentials NOT Provided!  Results of Scan May Not Be Accurate...")
            return False
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def service_detection(cnames, thisFqdn, logger):
    aws_empty_data = {
        "s3": [],
        "ec2": [],
        "cloudfront": [],
        "elb": [],
        "documentdb": [],
        "api_gateway": [],
        "elasticbeanstalk": [],
    }
    thisFqdn['aws'] = aws_empty_data
    gcp_empty_data = {
        "bucket": []
    }
    thisFqdn['gcp'] = gcp_empty_data
    print("[+] Starting Service Detection")
    print("------------------------------------")
    s3_pattern = r'(?:(?:[a-zA-Z0-9-]+\.)+s3(?:-website-[a-z0-9-]+)?\.amazonaws\.com)'
    ec2_pattern = r'.*(ec2|compute\.amazonaws\.com).*'
    cloudfront_pattern = r'.*(cloudfront\.net).*'
    elb_pattern = r'.*(elb\.amazonaws\.com).*'
    documentdb_pattern = r'\b\w+\.docdb\.amazonaws\.com\b'
    api_gateway_pattern = r'.*(execute-api\.[A-Za-z0-9.-]+\.amazonaws\.com).*'
    elasticbeanstalk_pattern = r'.*(elasticbeanstalk\.com).*'
    gcp_bucket_pattern = r'.*(storage\.googleapis\.com).*'
    counter = 0
    for cname in cnames:
        s3 = re.findall(s3_pattern, cname)
        ec2 = re.findall(ec2_pattern, cname)   
        cloudfront = re.findall(cloudfront_pattern, cname)
        elb = re.findall(elb_pattern, cname)
        documentdb = re.findall(documentdb_pattern, cname)
        api_gateway = re.findall(api_gateway_pattern, cname)
        elasticbeanstalk = re.findall(elasticbeanstalk_pattern, cname)
        gcp_bucket = re.findall(gcp_bucket_pattern, cname)

        if s3:
            new_s3 = {
                "domain":cname,
                "public":False,
                "downloadExploit":False,
                "uploadExploit":False,
                "authenticated":False,
                "subdomainTakeover":False,
            }
            thisFqdn['aws']['s3'].append(new_s3)
            print(f"[+] AWS S3 Bucket Found: {cname}")
            counter += 1
        elif ec2:
            thisFqdn['aws']['ec2'].append(cname)
            print(f"[+] AWS EC2 Instance Found: {cname}")
            counter += 1
        elif cloudfront:
            thisFqdn['aws']['cloudfront'].append(cname)
            print(f"[+] AWS Cloudfront Distribution Found: {cname}")
            counter += 1
        elif elb:
            new_elasticbeanstalk = {
                "domain":cname,
                "dangling":False
            }
            thisFqdn['aws']['elb'].append(new_elasticbeanstalk)
            print(f"[+] AWS ELB Found: {cname}")
            counter += 1
        elif documentdb:
            thisFqdn['aws']['documentdb'].append(cname)
            print(f"[+] AWS DocumentDB Found: {cname}")
            counter += 1
        elif api_gateway:
            thisFqdn['aws']['api_gateway'].append(cname)
            print(f"[+] AWS API Gateway Found: {cname}")
            counter += 1
        elif elasticbeanstalk:
            new_elasticbeanstalk = {
                "domain":cname,
                "subdomainTakeover":False
            }
            print(f"[+] AWS Elastic Beanstalk Found: {cname}")
            thisFqdn['aws']['elasticbeanstalk'].append(new_elasticbeanstalk)
            counter += 1
        elif gcp_bucket:
            new_gcp_bucket = {
                "domain": cname,
                "bucketSniping":False
            }
            print(f"[+] GCP Bucket Found: {cname}")
            thisFqdn['gcp']['bucket'].append(new_gcp_bucket)
            counter += 1
    test_gcp_bucket = {
        "domain": "pendo-eu-static-5739703306813440.storage.googleapis.com",
        "bucketSniping":False
    }
    thisFqdn['gcp']['bucket'].append(test_gcp_bucket)
    print(f"[-] Service Detection Complete!  {counter} Services Detected.")
    print("\n")
    logger.write_to_log("[MSG]","Fire-Cloud.py",f"Service Detection Completed Successfully!  {counter} Services Detected.")
    return thisFqdn

def s3_bucket_public(thisFqdn, logger):
    print("[+] Starting S3 Bucket Checks")
    print("------------------------------------")
    for bucket in thisFqdn['aws']['s3']:
        print(f"[-] Checking S3 bucket: {bucket['domain']} for public access")
        try:
            response = requests.get(f"http://{bucket['domain']}", timeout=5)
            if "ListBucketResult" in response.text:
                print(f"[!] Public access is open! Adding {bucket['domain']} to list of open buckets.\n")
                bucket['public'] = True
                logger.write_to_log("[MSG]","Fire-Cloud.py",f"Public S3 Bucket Discovered!  URL: {bucket['domain']}")
            else:
                print("[!] Public access does not appear to be open.")
                print("\n")
        except requests.exceptions.Timeout:
            print("[-] Request timed out. this may be a private bucket.")  
            print("\n")
        except requests.exceptions.RequestException as e:
            print(f"[!] An error occurred -- Bucket may be behind Cloudfront\n")
            print(f"[!] Exception: {e}")
    logger.write_to_log("[MSG]","Fire-Cloud.py",f"Public S3 Bucket Checks Completed Successfully!")
    return thisFqdn

def s3_bucket_authenticated(thisFqdn, logger):
    for bucket in thisFqdn['aws']['s3']:
        if bucket['public']:
            print(f"[-] Checking S3 bucket: {bucket['public']} for authenticated access using default aws profile")
            bucket_ls = subprocess.run(["aws", "s3", "ls", f"s3://{bucket['public']}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            if bucket_ls.returncode == 0:
                print(f"[!] Authenticated access is open! Dumping file names!")
                bucket['authenticated'] = True
                logger.write_to_log("[MSG]","Fire-Cloud.py",f"Public S3 Bucket Allowing Arbitrary Credentials Found!  URL: {bucket['public']}")
            else:
                print("[!] Authenticated access does not return any files.")
                print("\n")
    logger.write_to_log("[MSG]","Fire-Cloud.py",f"Authenticated S3 Bucket Checks Completed Successfully!")
    return thisFqdn

def s3_bucket_upload_exploit(thisFqdn, logger):
    for bucket in thisFqdn['aws']['s3']:
        print(f"[-] Attempting to exploit {bucket['public']} by uploading file")
        try:
            response = requests.put(f"http://{bucket['public']}/test.txt", data="test", timeout=5)
            if response.status_code == 200:
                bucket['uploadExploit'] = True
                print("[!] Exploit successful! File uploaded to bucket.")
                logger.write_to_log("[MSG]","Fire-Cloud.py",f"S3 File Upload Exploit Successful!  URL: {bucket['public']}")
            else:
                print("[-] Upload Exploit unsuccessful.")
        except requests.exceptions.Timeout:
            print("[-] Request timed out.")  
        except requests.exceptions.RequestException as e:
            print(f"[-] An error occurred -- check {bucket['public']} manually")
    logger.write_to_log("[MSG]","Fire-Cloud.py",f"File Upload Check on Public S3 Bucket Completed Successfully!")
    return thisFqdn

def s3_bucket_download_exploit(thisFqdn, logger):
    for bucket in thisFqdn['aws']['s3']:
        if bucket['public']:
            bucket_files = []
            print(f"[+] Listing contents of {bucket['domain']}")
            try:
                response = requests.get(f"http://{bucket['domain']}", timeout=5)
                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    key_elements = root.findall(".//{http://s3.amazonaws.com/doc/2006-03-01/}Contents/{http://s3.amazonaws.com/doc/2006-03-01/}Key")
                    file_names = [key.text for key in key_elements]
                    bucket['files'] = file_names
                    for file_name in file_names:
                        bucket_files.append(file_name)
                        print(f"[!] File found: {file_name}")
                    bucket['downloadExploit'] = True
                    logger.write_to_log("[MSG]","Fire-Cloud.py",f"S3 File Download Exploit Successful!  URL: {bucket['public']}")
                else:
                    print(f"[-] Unable to view files, check {bucket['domain']} manually.")
                print("\n")
            except requests.exceptions.Timeout:
                print("[-] Request timed out.")  
            except requests.exceptions.RequestException as e:
                print(f"[-] An error occurred -- check {bucket['domain']} manually")
    logger.write_to_log("[MSG]","Fire-Cloud.py",f"File Download Check on Public S3 Bucket Completed Successfully!")
    return thisFqdn

def s3_takover_exploit(thisFqdn, logger):
    print("[+] Checking S3 buckets and Cloudfront instances for S3 takeover")
    # https://hackingthe.cloud/aws/exploitation/orphaned_%20cloudfront_or_dns_takeover_via_s3/
    # This will check for the response "Bucket does not exist, which could lead to a subdomain takeover"
    # This will search known buckets and Cloudfront instances, but can be checked against any subdomain
    for bucket in thisFqdn['aws']['s3']:
        try: 
            response = requests.get(f"http://{bucket['domain']}", timeout=5)
            if "Bucket does not exist" in response.text:
                print(f"[!] Bucket deleted improperly, subdomain takeover may be possible on {bucket['domain']}")
                logger.write_to_log("[MSG]","Fire-Cloud.py",f"S3 Bucket May Be Vulnerable to Subdomain Takeover!  URL: {bucket['domain']}")
                bucket['subdomainTakeover'] = True
            else:
                print(f"[-] Bucket: {bucket['domain']} exists, not vulnerable")
        except requests.exceptions.Timeout:
            print("[-] Request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"[-] An error occurred -- check {bucket['domain']} manually")
    for cloudfront in thisFqdn['aws']['cloudfront']:
        try:
            response = requests.get(f"http://{cloudfront}", timeout=5)
            if "Bucket does not exist" in response.text:
                print(f"[!] Bucket deleted improperly, subdomain takeover may be possible on {cloudfront}")
            else:
                print(f"[-] Instance: {cloudfront} not vulnerable")
        except requests.exceptions.Timeout:
            print("[-] Request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"[-] An error occurred -- check {cloudfront} manually")
    logger.write_to_log("[MSG]","Fire-Cloud.py",f"AWS Service Subdomain Takeover Check Completed Successfully!")

def elb_checks(thisFqdn, logger):
    print("[+] Checking ELB instances for dangling CNAME")
    for elb in thisFqdn['aws']['elb']:
        try:
            response = requests.get(f"http://{elb['domain']}", timeout=5)
            if "NXDOMAIN" in response.text:
                print(f"[!] ELB appears to have been deleted improperly, investigate for additional impact {elb['domain']}")
                logger.write_to_log("[MSG]","Fire-Cloud.py",f"ELB with dangling CNAME!  URL: {elb['domain']}")
                elb['dangling'] = True
            else:
                print(f"[-] Instance: {elb['domain']} is not dangling")
                print(f"[-] Response: {response.text}")
        except requests.exceptions.Timeout:
            print(f"[-] Request timed out for {elb['domain']}.")
        except requests.exceptions.RequestException as e:
            print(f"[-] An error occurred -- check {elb['domain']} manually")
    logger.write_to_log("[MSG]","Fire-Cloud.py",f"ELB Dangling CNAME Check Completed Successfully!")

def ec2_checks(cname):
    print(f"[-] Checking EC2 instance: {cname}")
    try:
        response = requests.get(f"http://{cname}", timeout=5)
        if response.status_code == 200:
            print(f"[!] EC2 instance is accessible at {cname}")
        else:
            print(f"[-] EC2 instance is not accessible at {cname}")
    except requests.exceptions.Timeout:
        print("[-] Request timed out.")  
    except requests.exceptions.RequestException as e:
        print(f"[-] An error occurred -- check {cname} manually")
    ec2_nmap = subprocess.run(["nmap", "-Pn", "-p-", "-sT", "--reason", "--open", "-oA", "../temp/{cname}_tcp_full_port_scan", cname], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    if ec2_nmap.returncode == 0:
        print(f"[!] TCP Full Port Scan completed on {cname}")
    else:
        print(f"[-] TCP Full Port Scan failed on {cname}")

def beanstalk_takeover(thisFqdn, logger):
    print("[+] Checking Elastic Beanstalk instances for subdomain takeover")
    for beanstalk in thisFqdn['aws']['elasticbeanstalk']:
        try:
            response = requests.get(f"http://{beanstalk['domain']}", timeout=5)
            if "NXDOMAIN" in response.text:
                print(f"[!] Beanstalk appears to have been deleted improperly, subdomain takeover may be possible on {beanstalk}")
                logger.write_to_log("[MSG]","Fire-Cloud.py",f"Beanstalk instance May Be Vulnerable to Subdomain Takeover!  URL: {beanstalk['domain']}")
                beanstalk['subdomainTakeover'] = True
            else:
                print(f"[-] Instance: {beanstalk['domain']} not vulnerable")
        except requests.exceptions.Timeout:
            print("[-] Request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"[-] An error occurred -- check {beanstalk['domain']} manually")

def gcp_bucket_sniping(thisFqdn, logger):
    print("[+] Checking GCP buckets for takeover")
    for bucket in thisFqdn['gcp']['bucket']:
        try:
            response = requests.get(f"http://{bucket['domain']}", timeout=5)
            if "NoSuchBucket" in response.text:
                print(f"[!] GCP bucket appears vulnerable to takeover at {bucket['domain']}")
                logger.write_to_log("[MSG]","Fire-Cloud.py",f"GCP Bucket May Be Vulnerable to Subdomain Takeover!  URL: {bucket['domain']}")
            else:
                print(f"[-] GCP bucket is not vulnerable to takeover at {bucket['domain']}")
        except requests.exceptions.Timeout:
            print("[-] Request timed out.")  
        except requests.exceptions.RequestException as e:
            print(f"[-] An error occurred -- check {bucket['domain']} manually")

def get_fqdn_obj(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    return r.json()

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=False, default="127.0.0.1")
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=False, default="8000")
    parser.add_argument('-d','--fqdn', help='Name of the Root/Seed FQDN', required=True)
    return parser.parse_args() 

def get_cnames(fqdn):
    cname_list = []
    for fqdn in fqdn["dns"]['cnamerecord']:
        pattern = r"cname_record\s*-->\s*(.*?)\s*\("
        cname = re.findall(pattern, fqdn)
        cname_list.append(cname[0])
    return cname_list

def update_scan_progress(scan_step_name, target_domain):
    requests.post("http://localhost:5000/update-scan", json={"stepName":scan_step_name,"target_domain":target_domain})

def main(args):
    logger = Logger()
    thisFqdn = get_fqdn_obj(args)
    if args.fqdn:
        thisFqdn = get_fqdn_obj(args)
    cname_list = get_cnames(thisFqdn)
    aws_access_key_check(logger)
    update_scan_progress("Fire-Cloud | Service Detection", args.fqdn)
    thisFqdn = service_detection(cname_list, thisFqdn, logger)
    update_scan_progress("Fire-Cloud | S3 Bucket Detection", args.fqdn)
    thisFqdn = s3_bucket_public(thisFqdn, logger)
    update_scan_progress("Fire-Cloud | S3 Bucket Download", args.fqdn)
    s3_bucket_download_exploit(thisFqdn, logger)
    update_scan_progress("Fire-Cloud | S3 Bucket Default Creds", args.fqdn)
    s3_bucket_authenticated(thisFqdn, logger)
    update_scan_progress("Fire-Cloud | S3 Bucket Upload", args.fqdn)
    s3_bucket_upload_exploit(thisFqdn, logger)
    update_scan_progress("Fire-Cloud | S3 Bucket Takeover", args.fqdn)
    s3_takover_exploit(thisFqdn, logger)
    update_scan_progress("Fire-Cloud | Beanstalk Takeover", args.fqdn)
    beanstalk_takeover(thisFqdn, logger)
    update_scan_progress("Fire-Cloud | ELB Takeover", args.fqdn)
    elb_checks(thisFqdn, logger)
    update_scan_progress("Fire-Cloud | GCP Takeover", args.fqdn)
    gcp_bucket_sniping(thisFqdn, logger)
    update_fqdn_obj(args, thisFqdn)
    exit()

if __name__ == '__main__':
    args = arg_parse()
    main(args)