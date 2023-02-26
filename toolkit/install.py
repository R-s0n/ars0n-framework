import subprocess, argparse
from wildfire import Timer
from time import sleep

def tools_dir_check():
    home_dir = get_home_dir()
    go_check = subprocess.run([f"ls {home_dir}/Tools"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if go_check.returncode == 0:
        print("[+] Tools folder was found.")
        return True
    print("[!] Tools folder was NOT found.  Creating now...")
    return False

def create_tools_dir():
    home_dir = get_home_dir()
    subprocess.run([f"mkdir {home_dir}/Tools"], shell=True)
    install_check = subprocess.run([f"ls {home_dir}/Tools"], shell=True)
    if install_check.returncode == 0:
        print("[+] Tools directory successfully created.")
    else:
        print("[!] Tools directory was NOT successfully created!  Something is really jacked up.  Exiting...")
        exit()

def go_check():
    go_check = subprocess.run(["go version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if go_check.returncode == 0:
        print("[+] Go is already installed.")
        return True
    print("[!] Go is NOT already installed.  Installing now...")
    return False

def sublist3r_check():
    home_dir = get_home_dir()
    sublist3r_check = subprocess.run([f"python3 {home_dir}/Tools/Sublist3r/sublist3r.py --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if sublist3r_check.returncode == 0:
        print("[+] Sublist3r is already installed.")
        return True
    print("[!] Sublist3r is NOT already installed.  Installing now...")
    return False

def install_sublist3r():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir}/Tools; git clone https://github.com/aboul3la/Sublist3r.git"], shell=True)
    install_check = subprocess.run([f"python3 {home_dir}/Tools/Sublist3r/sublist3r.py --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] Sublist3r installed successfully!")
    else:
        print("[!] Something went wrong!  Sublist3r was NOT installed successfully...")

def assetfinder_check():
    home_dir = get_home_dir()
    assetfinder_check = subprocess.run([f"{home_dir}/go/bin/assetfinder --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if assetfinder_check.returncode == 0:
        print("[+] Assetfinder is already installed.")
        return True
    print("[!] Assetfinder is NOT already installed.  Installing now...")
    return False

def install_assetfinder():
    home_dir = get_home_dir()
    subprocess.run([f"go install github.com/tomnomnom/assetfinder@latest"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/assetfinder --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] Assetfinder installed successfully!")
    else:
        print("[!] Something went wrong!  Assetfinder was NOT installed successfully...")

def gau_check():
    home_dir = get_home_dir()
    gau_check = subprocess.run([f"{home_dir}/go/bin/gau --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if gau_check.returncode == 0:
        print("[+] Gau is already installed.")
        return True
    print("[!] Gau is NOT already installed.  Installing now...")
    return False

def install_gau():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir};wget https://github.com/lc/gau/releases/download/v2.1.2/gau_2.1.2_linux_amd64.tar.gz;tar xvf gau_2.1.2_linux_amd64.tar.gz;mv gau {home_dir}/go/bin/gau;rm gau_2.1.2_linux_amd64.tar.gz README.md LICENSE"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/gau --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] Gau installed successfully!")
    else:
        print("[!] Something went wrong!  Gau was NOT installed successfully...")

def shosubgo_check():
    home_dir = get_home_dir()
    shosubgo_check = subprocess.run([f"ls {home_dir}/Tools/shosubgo/"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if shosubgo_check.returncode == 0:
        print("[+] Shosubgo is already installed.")
        return True
    print("[!] Shosubgo is NOT already installed.  Installing now...")
    return False

def install_shosubgo():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir}/Tools;git clone https://github.com/incogbyte/shosubgo.git"], shell=True)
    install_check = subprocess.run([f"ls {home_dir}/Tools/shosubgo/"], shell=True)
    if install_check.returncode == 0:
        print("[+] Shosubgo installed successfully!  Don't forget to add your API key in the .keystore file.")
    else:
        print("[!] Something went wrong!  Shosubgo was NOT installed successfully...")

def crt_check():
    home_dir = get_home_dir()
    crt_check = subprocess.run([f"ls {home_dir}/Tools/tlshelpers/"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if crt_check.returncode == 0:
        print("[+] TLSHelpers is already installed.")
        return True
    print("[!] TLSHelpers is NOT already installed.  Installing now...")
    return False

def install_crt():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir}/Tools;git clone https://github.com/hannob/tlshelpers.git"], shell=True)
    install_check = subprocess.run([f"ls {home_dir}/Tools/tlshelpers/"], shell=True)
    if install_check.returncode == 0:
        print("[+] TLSHelpers installed successfully!")
    else:
        print("[!] Something went wrong!  TLSHelpers was NOT installed successfully...")

def subfinder_check():
    home_dir = get_home_dir()
    subfinder_check = subprocess.run([f"{home_dir}/go/bin/subfinder --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if subfinder_check.returncode == 0:
        print("[+] Subfinder is already installed.")
        return True
    print("[!] Subfinder is NOT already installed.  Installing now...")
    return False

def install_subfinder():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir};wget https://github.com/projectdiscovery/subfinder/releases/download/v2.5.4/subfinder_2.5.4_linux_amd64.zip;unzip subfinder_2.5.4_linux_amd64.zip;mv subfinder {home_dir}/go/bin/subfinder;rm subfinder_2.5.4_linux_amd64.zip README.md LICENSE"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/subfinder --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] Subfinder installed successfully!")
    else:
        print("[!] Something went wrong!  Subfinder was NOT installed successfully...")

def github_search_check():
    home_dir = get_home_dir()
    github_search_check = subprocess.run([f"ls {home_dir}/Tools/github-search/"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if github_search_check.returncode == 0:
        print("[+] GitHub-Search is already installed.")
        return True
    print("[!] GitHub-Search is NOT already installed.  Installing now...")
    return False

def install_github_search():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir}/Tools;git clone https://github.com/gwen001/github-search.git"], shell=True)
    install_check = subprocess.run([f"ls {home_dir}/Tools/github-search/"], shell=True)
    if install_check.returncode == 0:
        print("[+] GitHub-Search installed successfully!")
    else:
        print("[!] Something went wrong!  GitHub-Search was NOT installed successfully...")

def gospider_check():
    home_dir = get_home_dir()
    gospider_check = subprocess.run([f"{home_dir}/go/bin/gospider --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if gospider_check.returncode == 0:
        print("[+] GoSpider is already installed.")
        return True
    print("[!] GoSpider is NOT already installed.  Installing now...")
    return False

def install_gospider():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir};wget https://github.com/jaeles-project/gospider/releases/download/v1.1.6/gospider_v1.1.6_linux_x86_64.zip;unzip -j gospider_v1.1.6_linux_x86_64.zip;mv gospider {home_dir}/go/bin/gospider;rm gospider_v1.1.6_linux_x86_64.zip README.md LICENSE.md"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/gospider --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] GoSpider installed successfully!")
    else:
        print("[!] Something went wrong!  GoSpider was NOT installed successfully...")

def subdomainizer_check():
    home_dir = get_home_dir()
    subdomainizer_check = subprocess.run([f"ls {home_dir}/Tools/SubDomainizer/"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if subdomainizer_check.returncode == 0:
        print("[+] SubDomainizer is already installed.")
        return True
    print("[!] SubDomainizer is NOT already installed.  Installing now...")
    return False

def install_subdomainizer():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir}/Tools;git clone https://github.com/nsonaniya2010/SubDomainizer.git"], shell=True)
    install_check = subprocess.run([f"ls {home_dir}/Tools/SubDomainizer/"], shell=True)
    if install_check.returncode == 0:
        print("[+] SubDomainizer downloaded successfully!  Installing required modules...")
        subprocess.run([f"cd {home_dir}/Tools/SubDomainizer;pip3 install -r requirements.txt"], shell=True)
    else:
        print("[!] Something went wrong!  SubDomainizer was NOT installed successfully...")

def shuffledns_check():
    home_dir = get_home_dir()
    shuffledns_check = subprocess.run([f"{home_dir}/go/bin/shuffledns --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if shuffledns_check.returncode == 0:
        print("[+] ShuffleDNS is already installed.")
        return True
    print("[!] ShuffleDNS is NOT already installed.  Installing now...")
    return False

def install_shuffledns():
    home_dir = get_home_dir()
    subprocess.run([f"sudo apt-get install -y massdns;cd {home_dir};wget https://github.com/projectdiscovery/shuffledns/releases/download/v1.0.8/shuffledns_1.0.8_linux_amd64.zip;unzip shuffledns_1.0.8_linux_amd64.zip;mv shuffledns {home_dir}/go/bin/shuffledns;rm shuffledns_1.0.8_linux_amd64.zip README.md LICENSE.md"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/shuffledns --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] ShuffleDNS installed successfully!")
    else:
        print("[!] Something went wrong!  ShuffleDNS was NOT installed successfully...")

def httprobe_check():
    home_dir = get_home_dir()
    httprobe_check = subprocess.run([f"{home_dir}/go/bin/httprobe --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if httprobe_check.returncode == 0:
        print("[+] Httprobe is already installed.")
        return True
    print("[!] Httprobe is NOT already installed.  Installing now...")
    return False

def install_httprobe():
    home_dir = get_home_dir()
    subprocess.run([f"go install github.com/tomnomnom/httprobe@latest"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/httprobe --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] Httprobe installed successfully!")
    else:
        print("[!] Something went wrong!  Httprobe was NOT installed successfully...")

def tlsscan_check():
    home_dir = get_home_dir()
    tlsscan_check = subprocess.run([f"ls {home_dir}/Tools/tls-scan/tls-scan"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if tlsscan_check.returncode == 0:
        print("[+] TLS-Scan is already installed.")
        return True
    print("[!] TLS-Scan is NOT already installed.  Installing now...")
    return False

def install_tlsscan():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir};wget https://github.com/prbinu/tls-scan/releases/download/1.4.8/tls-scan-1.4.8-linux-amd64.tar.gz;tar xvf tls-scan-1.4.8-linux-amd64.tar.gz;mv tls-scan {home_dir}/Tools/tls-scan;rm tls-scan-1.4.8-linux-amd64.tar.gz"], shell=True)
    install_check = subprocess.run([f"ls {home_dir}/Tools/tls-scan/tls-scan"], shell=True)
    if install_check.returncode == 0:
        print("[+] TLS-Scan installed successfully!")
    else:
        print("[!] Something went wrong!  TLS-Scan was NOT installed successfully...")

def jq_check():
    jq_check = subprocess.run([f"jq --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if jq_check.returncode == 0:
        print("[+] JQ is already installed.")
        return True
    print("[!] JQ is NOT already installed.  Installing now...")
    return False

def install_jq():
    subprocess.run([f"sudo apt-get install -y jq "], shell=True)
    install_check = subprocess.run([f"jq --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] JQ installed successfully!")
    else:
        print("[!] Something went wrong!  JQ was NOT installed successfully...")

def dnmasscan_check():
    home_dir = get_home_dir()
    dnmasscan_check = subprocess.run([f"ls {home_dir}/Tools/dnmasscan/"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if dnmasscan_check.returncode == 0:
        print("[+] DNMasscan is already installed.")
        return True
    print("[!] DNMasscan is NOT already installed.  Installing now...")
    return False

def install_dnmasscan():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir}/Tools;git clone https://github.com/rastating/dnmasscan.git"], shell=True)
    install_check = subprocess.run([f"ls {home_dir}/Tools/dnmasscan/"], shell=True)
    if install_check.returncode == 0:
        print("[+] DNMasscan installed successfully!")
    else:
        print("[!] Something went wrong!  DNMasscan was NOT installed successfully...")

def nuclei_check():
    home_dir = get_home_dir()
    nuclei_check = subprocess.run([f"{home_dir}/go/bin/nuclei --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if nuclei_check.returncode == 0:
        print("[+] Nuclei is already installed.")
        return True
    print("[!] Nuclei is NOT already installed.  Installing now...")
    return False

def install_nuclei():
    home_dir = get_home_dir()
    subprocess.run([f"cd {home_dir};git clone https://github.com/projectdiscovery/nuclei-templates.git;wget https://github.com/projectdiscovery/nuclei/releases/download/v2.7.8/nuclei_2.7.8_linux_amd64.zip;unzip nuclei_2.7.8_linux_amd64.zip;mv nuclei {home_dir}/go/bin/nuclei;rm nuclei_2.7.8_linux_amd64.zip"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/nuclei --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] Nuclei installed successfully!")
    else:
        print("[!] Something went wrong!  Nuclei was NOT installed successfully...")

def install_go():
    # To Update: https://golang.org/doc/install
    home_dir = get_home_dir()
    subprocess.run([f"sudo apt-get update && sudo apt-get install -y golang-go; sudo apt-get install -y gccgo-go; mkdir {home_dir}/go;"], shell=True)
    install_check = subprocess.run(["go version"], shell=True)
    if install_check.returncode == 0:
        print("[+] Go installed successfully!")
    else:
        print("[!] Something went wrong!  Go was NOT installed successfully...")

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def keystore():
    home_dir = get_home_dir()
    keystore_check = subprocess.run([f"ls {home_dir}/.keys"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    if keystore_check.returncode == 0:
        print("[+] Keys directory found.")
    else:
        print("[!] Keys directory NOT found!  Creating now...")
        subprocess.run([f"mkdir {home_dir}/.keys"], shell=True)
        keystore_check = subprocess.run([f"ls {home_dir}/.keys"], shell=True)
        if keystore_check.returncode == 0:
            print("[+] Keys directory created successfully!")
            slack_key = input("[*] Please enter your Slack Token (ENTER to leave black and add later):\n")
            github_key = input("[*] Please enter your GitHub PAT (ENTER to leave black and add later):\n")
            shodan_key = input("[*] Please enter your Shodan API Key (ENTER to leave black and add later):\n")
            subprocess.run([f"""echo "{slack_key}" > {home_dir}/.keys/slack_web_hook && echo "github:{github_key}" > {home_dir}/.keys/.keystore && echo "shodan:{shodan_key}" >> {home_dir}/.keys/.keystore"""], shell=True)


def arg_parse():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=True)
    return parser.parse_args()

def main(args):
    print("[+] Starting install script")
    print("[!] WARNING: The install.py script should not be run as sudo.  If you did, ctrl+c and re-run the script as a user.  I'll give you a couple seconds ;)")
    sleep(2)
    starter_timer = Timer()
    keystore()
    if tools_dir_check() is False:
        create_tools_dir()
    if go_check() is False:
        install_go()
    if sublist3r_check() is False:
        install_sublist3r()
    if assetfinder_check() is False:
        install_assetfinder()
    if gau_check() is False:
        install_gau()
    if crt_check() is False:
        install_crt()
    if shosubgo_check() is False:
        install_shosubgo()
    if subfinder_check() is False:
        install_subfinder()
    if github_search_check() is False:
        install_github_search()
    if gospider_check() is False:
        install_gospider()
    if subdomainizer_check() is False:
        install_subdomainizer()
    if shuffledns_check() is False:
        install_shuffledns()
    if httprobe_check() is False:
        install_httprobe()
    if tlsscan_check() is False:
        install_tlsscan()
    if jq_check() is False:
        install_jq()
    if dnmasscan_check() is False:
        install_dnmasscan()
    if nuclei_check() is False:
        install_nuclei()
    starter_timer.stop_timer()
    print(f"[+] Done!  Start: {starter_timer.get_start()}  |  Stop: {starter_timer.get_stop()}")

if __name__ == "__main__":
    args = arg_parse()
    main(args)
