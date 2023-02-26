import requests, json

f = open(f'../wordlists/aws-ip-ranges.json')
aws_ips = json.load(f)
regions = []
for prefix in aws_ips['prefixes']:
    if prefix['region'] not in regions:
        regions.append(prefix['region'])
f.close()

print(regions)

for region in regions:
    try:
        r = requests.get(f"https://assets-sa-tech-de.s3.{region}.amazonaws.com", verify=False)
        code = str(r.status_code)
        print(f"{region} -- {code}")
        if code != "404":
            break
    except:
        continue


for region in regions:
    try:
        r = requests.get(f"https://s3.{region}.amazonaws.com/assets-sa-tech-de", verify=False)
        code = str(r.status_code)
        print(f"{region} -- {code}")
        if code != "404":
            break
    except:
        continue