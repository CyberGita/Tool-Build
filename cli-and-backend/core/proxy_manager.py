# core/proxy_manager.py

import random
import requests

class ProxyManager:
    def __init__(self, proxy_source=None):
        self.proxy_source = proxy_source or "https://www.proxy-list.download/api/v1/get?type=https"
        self.proxies = []
        self.load_proxies()

    def load_proxies(self):
        """Fetch proxies from the source URL."""
        print("[*] Fetching proxy list...")
        try:
            response = requests.get(self.proxy_source, timeout=10)
            if response.status_code == 200:
                self.proxies = list(set(response.text.strip().splitlines()))
                print(f"[+] Loaded {len(self.proxies)} proxies.")
            else:
                print("[-] Proxy list request failed.")
        except Exception as e:
            print(f"[-] Error fetching proxies: {e}")

    def get_random_proxy(self):
        """Return a random proxy string."""
        if not self.proxies:
            print("[-] No proxies loaded.")
            return None
        return random.choice(self.proxies)

    def format_proxy_dict(self, proxy):
        """Format proxy string for use with requests or Playwright."""
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
