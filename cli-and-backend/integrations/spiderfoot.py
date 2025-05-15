# integrations/spiderfoot.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPIDERFOOT_API = os.getenv("SPIDERFOOT_API", "http://localhost:5001")
SPIDERFOOT_API_KEY = os.getenv("SPIDERFOOT_API_KEY")

def push_to_spiderfoot(domain, emails, subdomains):
    if not SPIDERFOOT_API_KEY:
        print("[-] SpiderFoot API key missing in environment")
        return

    url = f"{SPIDERFOOT_API}/api/v1/scan/new"
    headers = {"Content-Type": "application/json"}
    payload = {
        "scan_type": "default",
        "seed": domain,
        "modules": ["sfp_email", "sfp_dns"],
        "options": {
            "_spiderfoot_api_key": SPIDERFOOT_API_KEY
        },
        "name": f"OSINTScan_{domain}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        scan_id = response.json().get("scan_id")
        print(f"[+] SpiderFoot scan started: ID {scan_id}")
    except Exception as e:
        print(f"[-] Error starting SpiderFoot scan: {e}")
