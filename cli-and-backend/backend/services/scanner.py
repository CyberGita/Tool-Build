from integrations.virustotal import check_subdomain_virustotal
from integrations.abuseipdb import resolve_to_ip, check_ip_abuse
from core.risk_scoring import calculate_risk_score, classify_risk
from core.browser_utils import fetch_with_redirect_handling

# TODO: Replace with actual subdomain/email harvesting logic
def dummy_scan(domain, sources):
    return ["sub1." + domain, "mail." + domain]

def run_scan(req):
    subdomains = dummy_scan(req.domain, req.sources)
    report = []

    
    for sub in subdomains:
        full_url = f"http://{sub}"
        page_result = fetch_with_redirect_handling(full_url)
        
        if page_result.get("status") == "error":
            continue  # skip or log error
        
        if "domaincntrol.com" in page_result["final_url"]:
            # Flag as parked
            report.append({
                "subdomain": sub,
                "status": "parked/redirected",
                "final_url": page_result["final_url"]
            })
            continue
    
    return {"domain": req.domain, "results": report}
