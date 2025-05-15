# modules/subdomain_crtsh.py

import requests
import json
import re

class CrtShScraper:
    def __init__(self, domain):
        self.domain = domain
        self.api_url = f"https://crt.sh/?q=%25.{domain}&output=json"

    def fetch_subdomains(self):
        try:
            print("[*] Querying crt.sh...")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            entries = json.loads(response.text)
            subdomains = set()

            for entry in entries:
                name_value = entry.get("name_value", "")
                for sub in name_value.split("\n"):
                    if sub.endswith(self.domain):
                        subdomains.add(sub.strip())

            return list(subdomains)
        except Exception as e:
            print(f"[-] crt.sh failed: {e}")
            return []
