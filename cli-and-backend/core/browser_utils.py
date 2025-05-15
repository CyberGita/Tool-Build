from playwright.sync_api import sync_playwright

def fetch_with_redirect_handling(url: str, timeout: int = 10000) -> dict:
    """
    Uses Playwright to handle JavaScript-based redirects and fetch final page content.
    Returns dict with final URL, status, and content.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="load", timeout=timeout)
            final_url = page.url
            content = page.content()
            browser.close()

        return {
            "final_url": final_url,
            "content": content,
            "status": "success"
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }
