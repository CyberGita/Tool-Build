from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "OSINT Threat Report", ln=True, align="C")

    def add_line(self, label, value):
        self.set_font("Arial", '', 12)
        self.cell(0, 10, f"{label}: {value}", ln=True)

def generate_pdf_report(data, filename="report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    for domain, ip, score, level in data:
        pdf.add_line("Subdomain", domain)
        pdf.add_line("IP", ip)
        pdf.add_line("Risk Score", score)
        pdf.add_line("Level", level)
        pdf.ln(5)
    pdf.output(filename)
    print(f"[+] PDF saved as {filename}")
