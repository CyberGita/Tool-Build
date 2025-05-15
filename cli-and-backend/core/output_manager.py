# core/output_manager.py

import json
import csv
import os

class OutputManager:
    def __init__(self, output_path="results", domain="output"):
        self.output_path = output_path
        self.domain = domain
        os.makedirs(output_path, exist_ok=True)

    def save_json(self, data):
        path = os.path.join(self.output_path, f"{self.domain}.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[+] JSON saved to: {path}")

    def save_csv(self, data):
        path = os.path.join(self.output_path, f"{self.domain}.csv")
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Value"])
            for email in data.get("emails", []):
                writer.writerow(["email", email])
            for sub in data.get("subdomains", []):
                writer.writerow(["subdomain", sub])
        print(f"[+] CSV saved to: {path}")

    def save_txt(self, data):
        path = os.path.join(self.output_path, f"{self.domain}.txt")
        with open(path, "w") as f:
            f.write("Emails:\n")
            for email in data.get("emails", []):
                f.write(email + "\n")
            f.write("\nSubdomains:\n")
            for sub in data.get("subdomains", []):
                f.write(sub + "\n")
        print(f"[+] TXT saved to: {path}")
