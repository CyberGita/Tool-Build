import argparse
import asyncio
from core.proxy_manager import ProxyManager
from core.browser_driver import BrowserDriver
from core.captcha_solver import CaptchaSolver
from modules.search_google import GoogleScraper
from modules.search_bing import BingScraper
from modules.subdomain_crtsh import CrtShScraper
from modules.subdomain_dnsdumpster import DNSDumpsterScraper
from core.output_manager import OutputManager
from modules.search_duckduckgo import DuckDuckGoScraper
from modules.search_yahoo import YahooScraper
from modules.search_fofa import FofaScraper
from modules.search_censys import CensysScraper
from modules.search_zoomeye import ZoomEyeScraper
from output.formatter import OutputFormatter
from integrations.spiderfoot import push_to_spiderfoot
from integrations.maltego import export_to_maltego_csv
from integrations.virustotal import check_subdomain_virustotal
from integrations.abuseipdb import resolve_to_ip, check_ip_abuse
from core.risk_scoring import calculate_risk_score, classify_risk
from reporting.email_alert import send_email_report
from reporting.slack_alert import send_slack_alert
from reporting.pdf_report import generate_pdf_report

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="🔍 Advanced OSINT Harvester: Email & Subdomain collector from multiple sources"
    )

    parser.add_argument(
        "--domain", "-d", required=True, help="Target domain (e.g. example.com)"
    )
    parser.add_argument(
        "--sources", "-s", default="google,bing,crtsh", 
        help="Comma-separated list of sources (default: google,bing,crtsh)"
    )
    parser.add_argument(
        "-o", "--output-format","--output",
        choices=["json", "csv", "txt","all"],
        default="json",
        help="Output format: json, csv, txt, all"
    )
    parser.add_argument(
        "--captcha-key", "-k", help="Optional 2Captcha API key for CAPTCHA solving"
    )
    parser.add_argument(
        "--use-proxy", action="store_true", help="Use public proxy for web requests"
    )
    parser.add_argument(
        "--user-agent",
        help="Custom User-Agent string (e.g. Brave, Arc, Googlebot)"
    )
    parser.add_argument("--spiderfoot", action="store_true", help="Push results to SpiderFoot")
    parser.add_argument("--maltego", action="store_true", help="Export results to Maltego CSV")
    parser.add_argument("--virustotal", action="store_true", help="Check subdomains on VirusTotal")
    parser.add_argument("--abuseipdb", action="store_true", help="Check subdomain IPs on AbuseIPDB")
    parser.add_argument("--email-report", action="store_true")
    parser.add_argument("--slack-report", action="store_true")
    parser.add_argument("--pdf-report", action="store_true")

    
    return parser.parse_args()

async def run_harvest(args):
    print(f"\n🌐 Target domain: {args.domain}")
    print(f"🔎 Using sources: {args.sources}")
    print(f"📁 Output format: {args.output_format}")
    
    proxy = None
    if args.use_proxy:
        print("[*] Proxy mode enabled.")
        proxy_mgr = ProxyManager()
        proxy = proxy_mgr.get_random_proxy()
        if proxy:
            print(f"[+] Selected proxy: {proxy}")
        else:
            print("[-] No proxy available. Continuing without proxy.")

    if args.captcha_key:
        print("[*] CAPTCHA solving enabled.")
        solver = CaptchaSolver(api_key=args.captcha_key)
        print("[i] 2Captcha will be used when a CAPTCHA is detected.")
        
    
    browser = BrowserDriver(proxy=proxy)
    html = await browser.fetch_page(f"https://www.google.com/search?q=site:{args.domain}")
    if html:
        print("[+] Sample page fetched. Begin parsing here...")

    # Placeholders for real scraping/enrichment functions
    print("\n[!] Scraping logic to be implemented here...")
    results = {"emails": set(), "subdomains": set()}
    sources = [s.strip().lower() for s in args.sources.split(",")]
    if "google" in sources:
        google = GoogleScraper(args.domain, proxy)
        emails, subs = await google.search()
        results["emails"].update(emails)
        results["subdomains"].update(subs)

    if "bing" in sources:
        bing = BingScraper(args.domain, proxy)
        emails, subs = await bing.search()
        results["emails"].update(emails)
        results["subdomains"].update(subs)
    if "duckduckgo" in sources:
        ddg = DuckDuckGoScraper(args.domain, proxy)
        emails, subs = await ddg.search()
        results["emails"].update(emails)
        results["subdomains"].update(subs)

    if "yahoo" in sources:
        y = YahooScraper(args.domain, proxy)
        emails, subs = await y.search()
        results["emails"].update(emails)
        results["subdomains"].update(subs)
        
    if "fofa" in sources:
        fofa = FofaScraper(args.domain)
        emails, subs = fofa.search()
        results["emails"].update(emails)
        results["subdomains"].update(subs)   
    
    if "censys" in sources:
        c = CensysScraper(args.domain)
        emails, subs = c.search()
        results["emails"].update(emails)
        results["subdomains"].update(subs)

    if "zoomeye" in sources:
        z = ZoomEyeScraper(args.domain)
        emails, subs = z.search()
        results["emails"].update(emails)
        results["subdomains"].update(subs)
          
    if "crtsh" in sources:
        crtsh = CrtShScraper(args.domain)
        subs = crtsh.fetch_subdomains()
        results["subdomains"].update(subs)

    if "dnsdumpster" in sources:
        dnsd = DNSDumpsterScraper(args.domain, proxy)
        subs = await dnsd.fetch_subdomains()
        results["subdomains"].update(subs) 
        print("\n📬 Emails found:", results["emails"])
        print("🌐 Subdomains found:", results["subdomains"])
    final_results = {
        "emails": list(results["emails"]),
        "subdomains": list(results["subdomains"])
    }

    out = OutputManager(domain=args.domain)
    if args.output_format == "json":
        out.save_json(final_results)
    elif args.output_format == "csv":
        out.save_csv(final_results)
    elif args.output_format == "txt":
        out.save_txt(final_results)
        
        
    formatter = OutputFormatter(final_results, args.domain)
    formatter.to_table()  

    if args.output_format == "json":
        formatter.to_json()
    elif args.output_format == "csv":
        formatter.to_csv()
    elif args.output_format == "txt":
        formatter.to_txt()
    elif args.output_format == "all":
        formatter.save_all()
        
        
    if args.spiderfoot:
        push_to_spiderfoot(args.domain, list(results["emails"]), list(results["subdomains"]))

    if args.maltego:
        export_to_maltego_csv(args.domain, list(results["emails"]), list(results["subdomains"]))
    
    if args.virustotal or args.abuseipdb:
        print("\n[bold yellow]Threat Intelligence Lookup[/bold yellow]")

        for sub in results["subdomains"]:
            if args.virustotal:
                vt_data = check_subdomain_virustotal(sub)
                print(f"[VT] {sub}: {vt_data}")

            if args.abuseipdb:
                ip = resolve_to_ip(sub)
                if ip:
                    abuse_data = check_ip_abuse(ip)
                    print(f"[ABUSEIPDB] {sub} ({ip}): {abuse_data}")
    risk_report = []
    for sub in results["subdomains"]:
        vt = check_subdomain_virustotal(sub) if args.virustotal else {}
        ip = resolve_to_ip(sub)
        abuse = check_ip_abuse(ip) if (ip and args.abuseipdb) else {}

        score = calculate_risk_score(vt, abuse)
        level = classify_risk(score)
        risk_report.append((sub, ip, score, level))

    if risk_report:
        print("\n[bold red]Threat Risk Report[/bold red]")
        from rich.table import Table
        table = Table(title="Risk Scores")

        table.add_column("Subdomain", style="cyan")
        table.add_column("IP", style="magenta")
        table.add_column("Risk Score", justify="center")
        table.add_column("Level", justify="center")

        for r in risk_report:
            table.add_row(*map(str, r))
        print(table)
        
    report_str = "\n".join([f"{d} ({ip}) -> Score: {s}, Level: {lvl}" for d, ip, s, lvl in risk_report])

    if args.email_report:
        send_email_report("OSINT Report", report_str, "recipient@example.com", os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))

    if args.slack_report:
        send_slack_alert(os.getenv("SLACK_WEBHOOK"), report_str)

    if args.pdf_report:
        generate_pdf_report(risk_report)     
            
            
def main():
    args = parse_arguments()
    asyncio.run(run_harvest(args))

if __name__ == "__main__":
    main()
