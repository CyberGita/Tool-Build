# modules/search_fofa.py

import os
import base64
import re
import requests
from dotenv import load_dotenv

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
SUBDOMAIN_REGEX_TEMPLATE = r"(?:[\w-]+\.)+{domain}"

class FofaScraper:
    def __init__(self, domain):
        load_dotenv()
        self.domain = domain
        self.email = os.getenv("FOFA_EMAIL")
        self.api_key = os.getenv("FOFA_API_KEY")
        self.base_url = "https://fofa.info/api/v1/search/all"

        if not self.email or not self.api_key:
            raise ValueError("FOFA_EMAIL or FOFA_API_KEY not found in env")

    def search(self):
        query = f'domain="{self.domain}"'
        b64_query = base64.b64encode(query.encode()).decode()
        url = f"{self.base_url}?email={self.email}&key={self.api_key}&qbase64={b64_query}&size=100"

        try:
            res = requests.get(url, timeout=15)
            res.raise_for_status()
            json_data = res.json()
            results = json_data.get("results", [])
            return self._parse(results)
        except Exception as e:
            print(f"[-] FOFA error: {e}")
            return [], []

    def _parse(self, results):
        emails = set()
        subdomains = set()
        subdomain_regex = re.compile(SUBDOMAIN_REGEX_TEMPLATE.format(domain=re.escape(self.domain)))

        for result in results:
            for field in result:
                if isinstance(field, str):
                    emails.update(re.findall(EMAIL_REGEX, field))
                    subdomains.update(subdomain_regex.findall(field))

        return list(emails), list(subdomains)
