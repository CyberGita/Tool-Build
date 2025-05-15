# integrations/maltego.py

import os
import csv
from datetime import datetime

def export_to_maltego_csv(domain, emails, subdomains, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{domain}_maltego.csv")

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Entity Type", "Value"])
        for email in sorted(set(emails)):
            writer.writerow(["maltego.EmailAddress", email])
        for sub in sorted(set(subdomains)):
            writer.writerow(["maltego.DNSName", sub])

    print(f"[+] Maltego CSV saved: {filename}")

