# modules/search_zoomeye.py

import os
import re
import requests
from dotenv import load_dotenv

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
SUBDOMAIN_REGEX_TEMPLATE = r"(?:[\w-]+\.)+{domain}"

class ZoomEyeScraper:
    def __init__(self, domain):
        load_dotenv()
        self.domain = domain
        self.token = os.getenv("ZOOMEYE_API_TOKEN")
        self.base_url = "https://api.zoomeye.org/host/search"

        if not self.token:
            raise ValueError("ZOOMEYE_API_TOKEN not found in env")

    def search(self):
        headers = {"Authorization": f"JWT {self.token}"}
        query = f"hostname:{self.domain}"

        try:
            res = requests.get(f"{self.base_url}?query={query}", headers=headers)
            res.raise_for_status()
            results = res.json().get("matches", [])
            return self._parse(results)
        except Exception as e:
            print(f"[-] ZoomEye error: {e}")
            return [], []

    def _parse(self, results):
        emails = set()
        subdomains = set()
        subdomain_regex = re.compile(SUBDOMAIN_REGEX_TEMPLATE.format(domain=re.escape(self.domain)))

        for entry in results:
            hostname = entry.get("hostname", "")
            portinfo = str(entry.get("portinfo", {}))
            for field in [hostname, portinfo]:
                if isinstance(field, str):
                    emails.update(re.findall(EMAIL_REGEX, field))
                    subdomains.update(subdomain_regex.findall(field))

        return list(emails), list(subdomains)
