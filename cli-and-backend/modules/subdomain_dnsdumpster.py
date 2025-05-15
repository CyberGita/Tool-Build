# modules/subdomain_dnsdumpster.py

import re
from core.browser_driver import BrowserDriver

class DNSDumpsterScraper:
    def __init__(self, domain, proxy=None):
        self.domain = domain
        self.proxy = proxy
        self.driver = BrowserDriver(proxy=self.proxy)

    async def fetch_subdomains(self):
        try:
            print("[*] Querying DNSDumpster...")
            url = "https://dnsdumpster.com"
            html = await self.driver.fetch_page(url)

            if not html:
                return []

            # Submit the form using page.evaluate() if needed
            page = await self.driver.context.new_page()
            await page.goto(url)
            await page.fill('input[name="targetip"]', self.domain)
            await page.click('input[type="submit"]')
            await page.wait_for_selector("table")

            final_html = await page.content()
            await page.close()

            # Extract subdomains
            subdomains = re.findall(r"([\w\.-]+\." + re.escape(self.domain) + r")", final_html)
            return list(set(subdomains))
        except Exception as e:
            print(f"[-] DNSDumpster failed: {e}")
            return []
