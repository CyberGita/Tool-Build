# modules/search_google.py

import re
from core.browser_driver import BrowserDriver

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
SUBDOMAIN_REGEX_TEMPLATE = r"(?:[\w-]+\.)+{domain}"

class GoogleScraper:
    def __init__(self, domain, proxy=None, user_agent=None):
        self.domain = domain
        self.proxy = proxy
        self.driver = BrowserDriver(proxy=self.proxy, user_agent=user_agent)

    async def search(self):
        query = f"site:{self.domain}"
        url = f"https://www.google.com/search?q={query}"
        html = await self.driver.fetch_page(url, wait_for_selector="body")
        if not html:
            return [], []

        emails = re.findall(EMAIL_REGEX, html)
        sub_regex = re.compile(SUBDOMAIN_REGEX_TEMPLATE.format(domain=re.escape(self.domain)))
        subdomains = list(set(sub_regex.findall(html)))

        return list(set(emails)), subdomains
