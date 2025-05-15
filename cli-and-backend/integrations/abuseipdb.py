# integrations/abuseipdb.py

import os
import requests
import socket
from dotenv import load_dotenv

load_dotenv()
ABUSE_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

def resolve_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def check_ip_abuse(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": ABUSE_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 30
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()["data"]
            return {
                "ip": ip,
                "abuseScore": data["abuseConfidenceScore"],
                "country": data.get("countryCode"),
                "isp": data.get("isp")
            }
        return {"ip": ip, "abuseScore": "N/A"}
    except Exception as e:
        return {"ip": ip, "error": str(e)}
