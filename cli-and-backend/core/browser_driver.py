# core/browser_driver.py

import asyncio
from playwright.async_api import async_playwright

import random

USER_AGENTS = [
    # Add more if needed
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
]


class BrowserDriver:
    def __init__(self, proxy=None, user_agent=None, browser_exe_path=None):
        self.proxy = proxy
        self.user_agent = user_agent
        self.browser_exe_path = browser_exe_path
        self.browser = None
        self.context = None

    async def init(self):
        self.playwright = await async_playwright().start()

        launch_args = {
            "headless": True,
            "args": ["--no-sandbox", "--disable-setuid-sandbox"]
        }

        if self.browser_exe_path:
            launch_args["executable_path"] = self.browser_exe_path

        self.browser = await self.playwright.chromium.launch(**launch_args)

        context_args = {}
        if self.user_agent:
            context_args["user_agent"] = self.user_agent

        if self.proxy:
            context_args["proxy"] = {"server": self.proxy}

        self.context = await self.browser.new_context(**context_args)

    async def fetch_page(self, url, wait_for_selector=None):
        await self.init()
        page = await self.context.new_page()
        try:
            await page.goto(url, timeout=20000)
            if wait_for_selector:
                await page.wait_for_selector(wait_for_selector, timeout=15000)
            html = await page.content()
        except Exception as e:
            print(f"[-] Page fetch failed: {e}")
            html = ""
        await self.close()
        return html

    async def close(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
