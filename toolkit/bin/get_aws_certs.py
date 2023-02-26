import subprocess

f = open("wordlists/tls_filtered.tmp")
ip_arr = f.read().split("\n")
print(ip_arr)

for ip in ip_arr:
    if len(ip) > 4:
        subprocess.run([f"amass intel -active -addr {ip}"], shell=True)