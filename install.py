import subprocess, argparse
from time import sleep
from datetime import datetime

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

def pip_check():
    pip_check = subprocess.run([f"pip3 --version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if pip_check.returncode == 0:
        print("[+] pip is already installed.")
        return True
    print("[!] pip is NOT installed.  Installing now...")
    return False

def install_pip():
    install_check = subprocess.run([f"sudo apt install python3-pip"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if install_check.returncode == 0:
        print("[+] pip was installed successfully!")
    else:
        print("[!] Something went wrong!  pip was NOT installed successfully...")  

def flask_cors_check():
    flask_cors_check = subprocess.run([f"pip3 show flask_cors"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if flask_cors_check.returncode == 0:
        print("[+] Flask_CORS is already installed.")
        return True
    print("[!] Flask_CORS is NOT installed.  Installing now...")
    return False

def install_flask_cors():
    install_check = subprocess.run([f"sudo apt install python3-flask-cors"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if install_check.returncode == 0:
        print("[+] Flask_CORS was installed successfully!")
    else:
        print("[!] Something went wrong!  Flask_CORS was NOT installed successfully...")    

def awscli_check():
    flask_cors_check = subprocess.run([f"aws --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if flask_cors_check.returncode == 0:
        print("[+] AWS CLI is already installed.")
        return True
    print("[!] AWS CLI is NOT installed.  Installing now...")
    return False

def install_awscli():
    install_check = subprocess.run([f"sudo apt install -y awscli"], shell=True)
    if install_check.returncode == 0:
        print("[+] AWS CLI was installed successfully!")
    else:
        print("[!] Something went wrong!  AWS CLI was NOT installed successfully...")    

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
    subprocess.run([f"cd {home_dir}/Tools; git clone https://github.com/huntergregal/Sublist3r.git; sudo apt install -y python3-requests python3-dnspython"], shell=True)
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
    subprocess.run([f"go install github.com/lc/gau/v2/cmd/gau@latest"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/gau --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] Gau installed successfully!")
    else:
        print("[!] Something went wrong!  Gau was NOT installed successfully...")

def shosubgo_check():
    home_dir = get_home_dir()
    shosubgo_check = subprocess.run([f"{home_dir}/go/bin/shosubgo --help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if shosubgo_check.returncode == 0:
        print("[+] Shosubgo is already installed.")
        return True
    print("[!] Shosubgo is NOT already installed.  Installing now...")
    return False

def install_shosubgo():
    home_dir = get_home_dir()
    subprocess.run([f"go install github.com/incogbyte/shosubgo@latest"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/shosubgo --help"], shell=True)
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
    subprocess.run([f"go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/subfinder --help"], shell=True)
    if install_check.returncode == 0:
        print("[+] Subfinder installed successfully!")
    else:
        print("[!] Something went wrong!  Subfinder was NOT installed successfully...")

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
    subprocess.run([f"GO111MODULE=on go install github.com/jaeles-project/gospider@latest"], shell=True)
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
        subprocess.run([f"cd {home_dir}/Tools/SubDomainizer;sudo apt install -y python3-termcolor python3-htmlmin python3-tldextract python3-colorama python3-cffi python3-bs4"], shell=True)
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
    subprocess.run([f"sudo apt-get install -y massdns; go install -v github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest"], shell=True)
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
    subprocess.run([f"cd {home_dir};wget https://github.com/prbinu/tls-scan/releases/download/1.6.0/tls-scan-1.6.0-linux-amd64.tar.gz;tar xvf tls-scan-1.6.0-linux-amd64.tar.gz;mv tls-scan {home_dir}/Tools/tls-scan;rm tls-scan-1.6.0-linux-amd64.tar.gz"], shell=True)
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
    subprocess.run([f"go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"], shell=True)
    install_check = subprocess.run([f"{home_dir}/go/bin/nuclei -update"], shell=True)
    if install_check.returncode == 0:
        print("[+] Nuclei installed successfully!")
    else:
        print("[!] Something went wrong!  Nuclei was NOT installed successfully...")

def install_go():
    home_dir = get_home_dir()
    subprocess.run([f"sudo apt install -y golang; export GOROOT=/usr/lib/go; export GOPATH=$HOME/go; export PATH=$GOPATH/bin:$GOROOT/bin:$PATH; source .zshrc"], shell=True)
    install_check = subprocess.run(["go version"], shell=True)
    if install_check.returncode == 0:
        print("[+] Go installed successfully!")
    else:
        print("[!] Something went wrong!  Go was NOT installed successfully...")

def node_check():
    node_check = subprocess.run([f"node --version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    if node_check.returncode == 0:
        print("[+] Node is already installed.")
        return True
    print("[!] Node is NOT already installed.  Installing now...")
    print("[!] This can take 30+ minutes depending on your machine.")
    return False

def install_node():
    node_install = subprocess.run(["sudo apt-get install -y nodejs;"], shell=True)
    if node_install.returncode == 0:
        print("[+] Node was installed successfully!")
    else:
        print("[!] Something went wrong!  Node 18 was NOT installed successfully...")

def npm_check():
    npm_check = subprocess.run([f"npm --version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    if npm_check.returncode == 0:
        print("[+] NPM is already installed.  Checking version...")
        npm_version = npm_check.stdout.split(".")[0]
        print(f"[-] Current NPM Version: {npm_version}")
        if npm_version == "9":
            print("[+] NPM 9 is already installed.")
            return True
    print("[!] npm 9 is NOT already installed.  Installing now...")
    print("[!] This can take 30+ minutes depending on your machine.")
    return False

def install_npm():
    npm_install = subprocess.run(["sudo apt-get install npm -y"], shell=True)
    if npm_install.returncode == 0:
        print("[+] NPM 9 was installed successfully!")
    else:
        print("[!] Something went wrong!  NPM 9 was NOT installed successfully...")

def kali_mongodb_check():
    kali_mongodb_check = subprocess.run(['sudo docker exec mongodb-container mongosh --eval "db.runCommand({ connectionStatus: 1 })"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if kali_mongodb_check.returncode == 0:
        print("[+] Mongodb is already installed.")
        return True
    print("[!] Mongodb is NOT already installed.  Installing now...")
    return False

def kali_install_mongodb():
    subprocess.run(["""sudo apt install docker.io -y; sudo systemctl start docker; sudo systemctl enable docker; sudo docker pull mongo; sudo docker run -d -p 27017:27017 --name mongodb-container mongo; """], shell=True)
    sleep(2)
    final_kali_mongodb_check = subprocess.run(['sudo docker exec mongodb-container mongosh --eval "db.runCommand({ connectionStatus: 1 })"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if final_kali_mongodb_check.returncode == 0:
        print("[+] MongoDB was installed successfully!")
    else:
        print("[!] Something went wrong!  MongoDB was NOT installed successfully...")

def docker_mongodb_check():
    docker_mongodb_check = subprocess.run(['mongosh --eval "db.runCommand({ connectionStatus: 1 })"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if docker_mongodb_check.returncode == 0:
        print("[+] Mongodb is already installed.")
        return True
    print("[!] Mongodb is NOT already installed.  Installing now...")
    return False

def docker_install_mongodb():
    subprocess.run(["""sudo apt install docker.io -y; sudo systemctl start docker; sudo systemctl enable docker; sudo docker pull mongo; sudo docker run -d -p 27017:27017 --name mongodb-container mongo; """], shell=True)
    sleep(2)
    final_docker_mongodb_check = subprocess.run(['sudo docker exec mongodb-container mongosh --eval "db.runCommand({ connectionStatus: 1 })"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if final_docker_mongodb_check.returncode == 0:
        print("[+] MongoDB was installed successfully!")
    else:
        print("[!] Something went wrong!  MongoDB was NOT installed successfully...")

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
            hackerone_user = input("[*] Please enter your HackerOne Username (ENTER to leave black and add later):\n")
            hackerone_key = input("[*] Please enter your HackerOne API Key (ENTER to leave black and add later):\n")
            subprocess.run([f"""echo "{hackerone_user}:{hackerone_key}" > {home_dir}/.keys/.hackerone && echo "{slack_key}" > {home_dir}/.keys/slack_web_hook && echo "github:{github_key}" > {home_dir}/.keys/.keystore && echo "shodan:{shodan_key}" >> {home_dir}/.keys/.keystore"""], shell=True)

def server_check():
    server_check = subprocess.run([f"ls server/node_modules"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if server_check.returncode == 0:
        print("[+] The Ars0n Framework Server is already installed.")
        return True
    print("[!] The Ars0n Framework Server is NOT already installed.  Installing now...")
    return False

def client_check():
    client_check = subprocess.run([f"ls client/node_modules"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if client_check.returncode == 0:
        print("[+] The Ars0n Framework Client is already installed.")
        return True
    print("[!] The Ars0n Framework Client is NOT already installed.  Installing now...")
    return False

def install_server():
    server_install = subprocess.run(["cd server; npm install"], shell=True)
    if server_install.returncode == 0:
        print("[+] The Ars0n Framework Server was installed successfully!")
    else:
        print("[!] Something went wrong!  The Ars0n Framework Server was NOT installed successfully...")

def install_client():
    client_install = subprocess.run(["cd client; npm install"], shell=True)
    if client_install.returncode == 0:
        print("[+] The Ars0n Framework Client was installed successfully!")
    else:
        print("[!] Something went wrong!  The Ars0n Framework Client was NOT installed successfully...")

def run_server_prompt():
    prompt = input("[?] Would you like to run the web application now? (Y/n)")
    if prompt.lower() == "y":
        subprocess.run(["chmod 777 run.sh; ./run.sh"], shell=True)

def update_apt():
    subprocess.run(["sudo apt-get update"], stdout=subprocess.DEVNULL, shell=True)

def install_protonvpn():
    home_dir = get_home_dir()
    download_protonvpn = subprocess.run([f'cd {home_dir}/Downloads;wget "https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_1.0.3_all.deb";sudo apt-get install ~/Downloads/protonvpn-stable-release_1.0.3_all.deb;sudo apt-get update;sudo apt-get install protonvpn -y'], shell=True)
    if download_protonvpn.returncode == 0:
        print("[+] ProtonVPN was installed successfully!")
    else:
        print("[!] Something went wrong!  ProtonVPN was NOT installed successfully...")    

def stray_license_file():
    home_dir = get_home_dir()
    subprocess.run([f"rm -f {home_dir}/LICENSE* {home_dir}/README*"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vpn', help='Install ProtonVPN Debian Client - https://protonvpn.com', required=False, action='store_true')
    return parser.parse_args()

def validate_install():
    print("[-] Validating installation...")
    checks = [
        tools_dir_check,
        flask_cors_check,
        awscli_check,
        node_check,
        npm_check,
        kali_mongodb_check,
        go_check,
        sublist3r_check,
        assetfinder_check,
        gau_check,
        crt_check,
        shosubgo_check,
        subfinder_check,
        gospider_check,
        subdomainizer_check,
        shuffledns_check,
        httprobe_check,
        tlsscan_check,
        jq_check,
        dnmasscan_check,
        nuclei_check,
        server_check,
        client_check
    ]
    for check in checks:
        if not check():
            return False
    stray_license_file()
    return True

def main(args):
    print("[+] Starting install script")
    starter_timer = Timer()
    # keystore()
    update_apt()
    failed_check_count = 0
    if pip_check() is False:
        failed_check_count += 1
        install_pip()
    if tools_dir_check() is False:
        failed_check_count += 1
        create_tools_dir()
    if flask_cors_check() is False:
        failed_check_count += 1
        install_flask_cors()
    if awscli_check() is False:
        failed_check_count += 1
        install_awscli()
    if node_check() is False:
        failed_check_count += 1
        install_node()
    if npm_check() is False:
        failed_check_count += 1
        install_npm()
    if kali_mongodb_check() is False:
        failed_check_count += 1
        kali_install_mongodb()
    # if go_check() is False:
    #     failed_check_count += 1
    #     install_go()
    # if sublist3r_check() is False:
    #     failed_check_count += 1
    #     install_sublist3r()
    # if assetfinder_check() is False:
    #     failed_check_count += 1
    #     install_assetfinder()
    # if gau_check() is False:
    #     failed_check_count += 1
    #     install_gau()
    # if crt_check() is False:
    #     failed_check_count += 1
    #     install_crt()
    # if shosubgo_check() is False:
    #     failed_check_count += 1
    #     install_shosubgo()
    # if subfinder_check() is False:
    #     failed_check_count += 1
    #     install_subfinder()
    # if gospider_check() is False:
    #     failed_check_count += 1
    #     install_gospider()
    # if subdomainizer_check() is False:
    #     failed_check_count += 1
    #     install_subdomainizer()
    # if shuffledns_check() is False:
    #     failed_check_count += 1
    #     install_shuffledns()
    # if httprobe_check() is False:
    #     failed_check_count += 1
    #     install_httprobe()
    # if tlsscan_check() is False:
    #     failed_check_count += 1
    #     install_tlsscan()
    # if jq_check() is False:
    #     failed_check_count += 1
    #     install_jq()
    # if dnmasscan_check() is False:
    #     failed_check_count += 1
    #     install_dnmasscan()
    # if nuclei_check() is False:
    #     failed_check_count += 1
    #     install_nuclei()
    # if server_check() is False:
    #     failed_check_count += 1
    #     install_server()
    # if client_check() is False:
    #     failed_check_count += 1
    #     install_client()
    # if failed_check_count > 0:
    #     if validate_install() is False:
    #         print("[!] Something went wrong!  Please try to run the installer again or open an issue on the repo...")
    #         exit()
    starter_timer.stop_timer()
    # run_server_prompt()
    print(f"[+] Done!  Start: {starter_timer.get_start()}  |  Stop: {starter_timer.get_stop()}")

if __name__ == "__main__":
    args = arg_parse()
    main(args)
