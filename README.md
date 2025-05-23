# 🕵️‍♂️ OSINT-Harvester

**OSINT-Harvester** is an advanced Python-based command-line and API-driven tool for harvesting emails, subdomains, and intelligence from multiple data sources. It includes CAPTCHA bypassing, proxy support, browser emulation, and risk scoring via VirusTotal and AbuseIPDB. The tool integrates with SpiderFoot, Maltego, FOFA, ZoomEye, and Censys.

---

## 🚀 Features

- ✅ Email & Subdomain Harvesting:
  - Search Engines: Google, Bing, Yahoo, DuckDuckGo
  - Certificate Transparency: crt.sh
  - DNS Discovery: DNSDumpster

- 🧠 Intelligence & Scoring:
  - VirusTotal domain/IP scoring
  - AbuseIPDB abuse classification
  - Risk-level output

- 🧩 Tool Integrations:
  - SpiderFoot (API)
  - Maltego (export & transforms)

- 🧱 Modular Architecture:
  - Browser-based scraping (Playwright)
  - Proxy rotation
  - CAPTCHA solving (2Captcha, AntiCaptcha)
  - User-Agent spoofing

- 🖥️ Custom Output:
  - Formats: JSON, CSV, PDF, TXT
  - Slack/Email alerts

- ⚡ FastAPI Backend:
  - REST API for remote or frontend access

---

## 📦 Installation

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/osint-harvester.git
cd osint-harvester
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers**

```bash
playwright install
```

## 🔐 Environment Setup

Create a .env file in the root directory with the following:
```env
VT_API_KEY=your_virustotal_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
SPIDERFOOT_API_KEY=your_spiderfoot_key
FOFA_EMAIL=your_email
FOFA_KEY=your_fofa_key
SHODAN_API_KEY=your_shodan_key
CENSYS_API_ID=your_censys_id
CENSYS_API_SECRET=your_censys_secret
2CAPTCHA_API_KEY=your_2captcha_key
```

## 🧪 CLI Usage
```bash
python harvest_tool.py --domain example.com --sources google,bing,crtsh --output json
```

### CLI Options
| Option       | Description                                |
| ------------ | ------------------------------------------ |
| `--domain`   | Target domain (e.g., example.com)          |
| `--sources`  | Comma-separated list of sources            |
| `--output`   | Output format: `json`, `csv`, `pdf`, `txt` |
| `--proxy`    | Enable proxy rotation                      |
| `--headless` | Run in headless browser mode               |

## 🌐 FastAPI Backend

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Sample API Request (POST /api/scan)

```json
{
  "domain": "example.com",
  "sources": ["google", "crtsh"],
  "use_virustotal": true,
  "use_abuseipdb": true,
  "output_format": "json"
}
```

## 📤 Output Options

- Console display via rich

- JSON, CSV, PDF, or TXT files

- Slack/Email alerts (optional)

## 🔍 Supported Sources

- ### Search Engines
    - Google
    - Bing
    - Yahoo
    - DuckDuckGo

- ### DNS & Certificates

    - crt.sh
    - DNSDumpster
    - Censys

- ### APIs & Directories

    - FOFA
    - Shodan
    - ZoomEye

## 🔄 Integration Support

| Tool       | Support Type       |
| ---------- | ------------------ |
| SpiderFoot | API integration    |
| Maltego    | Export & transform |
| VirusTotal | Domain/IP scoring  |
| AbuseIPDB  | IP abuse lookup    |

## 🛡️ CAPTCHA & Redirects

- JavaScript redirect handling
- CAPTCHA solving:
    - ✅ 2Captcha
    - ✅ AntiCaptcha
- Headless Playwright emulation
- Modern browser support (Chrome, Brave, Arc)

## 🔧 Developer Tools

- Proxy support
- .env config manager
- Modular plugins
- Graceful error handling
- Extendable data pipelines

