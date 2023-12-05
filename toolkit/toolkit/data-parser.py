import requests
import argparse
import re

def get_fqdn_obj(args):
    r = requests.post(
        f'http://{args.server}:{args.port}/api/auto', data={'fqdn': args.fqdn})
    return r.json()

def parse_arecords(fqdn):
    ip_list = []
    for ip in fqdn['dns']['arecord']:
        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ip = re.findall(pattern, ip)
        ip_list.append(ip[0])
    return ip_list

def parse_subs(fqdn):
    sub_list = []
    for key in fqdn['recon']['subdomains']:
        for subdomain in fqdn['recon']['subdomains'][key]:
            sub_list.append(subdomain)
    return sub_list

def parse_cnames(fqdn):
    cname_list = []
    for fqdn in fqdn['dns']['cnamerecord']:
        pattern = r"cname_record\s*-->\s*(.*?)\s*\("
        cname = re.findall(pattern, fqdn)
        cname_list.append(cname[0])
    return cname_list

def write_data_to_file(data_list, filename):
    try:
        with open(filename, 'w') as file:
            for key in data_list:
                file.write(key + '\n')
        print(f"Data has been written to {filename}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S', '--server', help='IP Address of MongoDB API',
                        required=False, default="127.0.0.1")
    parser.add_argument(
        '-P', '--port', help='Port of MongoDB API', required=False, default="8000")
    parser.add_argument(
        '-d', '--fqdn', help='Name of the Root/Seed FQDN', required=True)
    parser.add_argument('-s', '--subdomains', help='Return list of subdomains', required=False, action='store_true')
    parser.add_argument('-i', '--ip', help='Return a list of IPs', required=False, action='store_true')
    parser.add_argument('-c', '--cname', help='Return a list of cloud resources', required=False, action='store_true')
    parser.add_argument('-f', '--file', help='File to write data to', required=False, default=f"../temp/data.txt")
    return parser.parse_args()

def main(args):
    thisFqdn = get_fqdn_obj(args)
    if args.ip:
        parsed_ips = parse_arecords(thisFqdn)
        write_data_to_file(parsed_ips, args.file)
    if args.subdomains:
        parsed_subs = parse_subs(thisFqdn)
        write_data_to_file(parsed_subs, args.file)
    if args.cname:
        parsed_cnames = parse_cnames(thisFqdn)
        write_data_to_file(parsed_cnames, args.file)

if __name__ == '__main__':
    args = arg_parse()
    main(args)
