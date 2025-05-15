# modules/search_censys.py

import os
import re
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
SUBDOMAIN_REGEX_TEMPLATE = r"(?:[\w-]+\.)+{domain}"

class CensysScraper:
    def __init__(self, domain):
        load_dotenv()
        self.domain = domain
        self.api_id = os.getenv("CENSYS_API_ID")
        self.api_secret = os.getenv("CENSYS_API_SECRET")
        self.base_url = "https://search.censys.io/api/v2"

        if not self.api_id or not self.api_secret:
            raise ValueError("CENSYS_API_ID or CENSYS_API_SECRET missing in env")

    def search(self):
        url = f"{self.base_url}/hosts/search"
        query = {"q": f"{self.domain}", "per_page": 100}

        try:
            res = requests.post(url, json=query, auth=HTTPBasicAuth(self.api_id, self.api_secret))
            res.raise_for_status()
            results = res.json().get("result", {}).get("hits", [])
            return self._parse(results)
        except Exception as e:
            print(f"[-] Censys error: {e}")
            return [], []

    def _parse(self, results):
        emails = set()
        subdomains = set()
        subdomain_regex = re.compile(SUBDOMAIN_REGEX_TEMPLATE.format(domain=re.escape(self.domain)))

        for hit in results:
            ip = hit.get("ip", "")
            names = hit.get("names", [])
            location = str(hit.get("location", ""))

            for item in [ip] + names + [location]:
                if isinstance(item, str):
                    emails.update(re.findall(EMAIL_REGEX, item))
                    subdomains.update(subdomain_regex.findall(item))

        return list(emails), list(subdomains)
