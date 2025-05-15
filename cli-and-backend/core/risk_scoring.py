# core/risk_scoring.py

def calculate_risk_score(vt_result, abuse_result):
    vt_malicious = vt_result.get("malicious", 0)
    vt_suspicious = vt_result.get("suspicious", 0)
    abuse_score = abuse_result.get("abuseScore", 0)

    # Risk weight logic (scale: 0–100)
    score = (vt_malicious * 10) + (vt_suspicious * 5) + (abuse_score * 1)

    # Cap at 100
    return min(score, 100)

def classify_risk(score):
    if score >= 80:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"
