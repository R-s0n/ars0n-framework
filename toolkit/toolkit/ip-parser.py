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


def write_ips_to_file(ip_list, filename):
    try:
        with open(filename, 'w') as file:
            for ip in ip_list:
                file.write(ip + '\n')
        print(f"IP addresses have been written to {filename}")
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
    return parser.parse_args()


def main(args):
    if args.fqdn:
        thisFqdn = get_fqdn_obj(args)
    parsed_ips = parse_arecords(thisFqdn)
    write_ips_to_file(parsed_ips, f"../temp/{args.fqdn}.txt")


if __name__ == '__main__':
    args = arg_parse()
    main(args)
