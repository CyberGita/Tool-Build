# core/captcha_solver.py

import time
import requests

class CaptchaSolver:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_base = "http://2captcha.com"

    def solve_recaptcha_v2(self, site_key, page_url):
        print("[*] Sending CAPTCHA to 2Captcha...")
        payload = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url,
            'json': 1
        }
        resp = requests.post(f"{self.api_base}/in.php", data=payload)
        if resp.status_code != 200 or resp.json().get("status") != 1:
            print("[-] Failed to submit CAPTCHA.")
            return None

        request_id = resp.json().get("request")
        print(f"[+] CAPTCHA submitted. Request ID: {request_id}")

        # Poll for solution
        for attempt in range(20):
            time.sleep(5)
            check_payload = {'key': self.api_key, 'action': 'get', 'id': request_id, 'json': 1}
            check_resp = requests.get(f"{self.api_base}/res.php", params=check_payload)
            if check_resp.json().get("status") == 1:
                solution = check_resp.json().get("request")
                print("[+] CAPTCHA solved.")
                return solution
            elif "CAPCHA_NOT_READY" in check_resp.text:
                print("[*] CAPTCHA not ready, waiting...")
            else:
                print("[-] Error retrieving CAPTCHA solution:", check_resp.text)
                break
        return None
