# integrations/virustotal.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
VT_API_KEY = os.getenv("VT_API_KEY")
VT_URL = "https://www.virustotal.com/api/v3"

def check_subdomain_virustotal(subdomain):
    headers = {
        "x-apikey": VT_API_KEY
    }

    try:
        url = f"{VT_URL}/domains/{subdomain}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            return {"domain": subdomain, "score": "N/A", "harmless": 0, "malicious": 0}

        data = resp.json().get("data", {}).get("attributes", {})
        stats = data.get("last_analysis_stats", {})
        malicious = stats.get("malicious", 0)
        harmless = stats.get("harmless", 0)
        suspicious = stats.get("suspicious", 0)
        return {
            "domain": subdomain,
            "malicious": malicious,
            "suspicious": suspicious,
            "harmless": harmless
        }
    except Exception as e:
        return {"domain": subdomain, "error": str(e)}
