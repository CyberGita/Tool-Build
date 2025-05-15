# output/formatter.py

import os
import json
import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


class OutputFormatter:
    def __init__(self, data, domain, output_dir="results"):
        self.data = data
        self.domain = domain
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _safe_filename(self, ext):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"{self.domain}_{timestamp}.{ext}")

    def to_json(self):
        path = self._safe_filename("json")
        with open(path, "w") as f:
            json.dump(self.data, f, indent=4)
        console.print(f"[green][+][/green] JSON saved: {path}")

    def to_csv(self):
        path = self._safe_filename("csv")
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Value"])
            for email in sorted(set(self.data["emails"])):
                writer.writerow(["Email", email])
            for subdomain in sorted(set(self.data["subdomains"])):
                writer.writerow(["Subdomain", subdomain])
        console.print(f"[green][+][/green] CSV saved: {path}")

    def to_txt(self):
        path = self._safe_filename("txt")
        with open(path, "w") as f:
            f.write("[Emails]\n")
            for email in sorted(set(self.data["emails"])):
                f.write(email + "\n")
            f.write("\n[Subdomains]\n")
            for sub in sorted(set(self.data["subdomains"])):
                f.write(sub + "\n")
        console.print(f"[green][+][/green] TXT saved: {path}")

    def to_table(self):
        console.print("\n[bold underline]Harvested Results[/bold underline]\n")

        if self.data["emails"]:
            table = Table(title="Emails")
            table.add_column("Email", style="cyan")
            for email in sorted(set(self.data["emails"])):
                table.add_row(email)
            console.print(table)

        if self.data["subdomains"]:
            table = Table(title="Subdomains")
            table.add_column("Subdomain", style="magenta")
            for sub in sorted(set(self.data["subdomains"])):
                table.add_row(sub)
            console.print(table)

    def save_all(self):
        self.to_json()
        self.to_csv()
        self.to_txt()
