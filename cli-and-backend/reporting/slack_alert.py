import requests

def send_slack_alert(webhook_url, message):
    payload = {"text": message}
    resp = requests.post(webhook_url, json=payload)
    if resp.status_code == 200:
        print("[+] Slack alert sent.")
    else:
        print(f"[-] Slack failed: {resp.status_code}")
