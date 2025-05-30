import asyncio
from playwright.async_api import async_playwright
import random

LINKS = [
    "https://recentlathe.com/xpy2ss5b?key=76ef28c776bf7442b072814fe9b9fadc",
    "https://recentlathe.com/c5rbc5p8a?key=226b416b80913b8048c934360317a81e",
    "https://recentlathe.com/pvsbr23z?key=8424135d37def77e5dfd6a4bc2093c0f",
    "https://recentlathe.com/setc75v4n?key=27dc1b007080764c99d048867e05e576",
    "https://recentlathe.com/kbams22pg?key=9acb3011f54c6550d334d582c517e2eb",
    "https://recentlathe.com/t74529mmr?key=30c25c576f0c276c4a22df808747f71d",
    "https://recentlathe.com/ms1m9ydzxp?key=9235ec7e77ffa9f4763f1bd948ee81f9",
    "https://recentlathe.com/srv31xydpw?key=8781d8882bae3f018bf88b7622434581",
    "https://recentlathe.com/mgjjfkmfie?key=45ca6af141bc01cdeacbd46dfaef7e2a"
]

# 🎯 Click function
async def do_random_clicks(page, max_clicks=3):
    elements = await page.query_selector_all("a, button, [role='button'], [onclick], [tabindex]")
    if not elements:
        print("[-] No clickable elements found.")
        return

    random.shuffle(elements)
    to_click = elements[:random.randint(1, min(max_clicks, len(elements)))]

    for el in to_click:
        try:
            box = await el.bounding_box()
            if box:
                print(f"[+] Clicking on element at ({int(box['x'])}, {int(box['y'])})")
                await el.click(timeout=5000)
                await page.wait_for_timeout(random.randint(2000, 4000))  # wait after each click
        except Exception as e:
            print(f"[!] Click failed: {e}")

# 🧭 Main function
async def visit_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # ✅ Headless: No visual browser
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for url in LINKS:
            try:
                print(f"\n[🌐] Visiting: {url}")
                await page.goto(url, timeout=60000)

                # Wait like a human reading
                wait_time = random.randint(5000, 10000)
                print(f"[*] Reading page for {wait_time/1000} seconds...")
                await page.wait_for_timeout(wait_time)

                # Simulate scrolling slowly
                for _ in range(random.randint(3, 6)):
                    scroll_distance = random.randint(300, 900)
                    await page.mouse.wheel(0, scroll_distance)
                    await page.wait_for_timeout(random.randint(1200, 2500))

                # Wait again before clicks
                await page.wait_for_timeout(random.randint(2000, 5000))

                # Clicks
                await do_random_clicks(page)

                # Final delay before next URL
                cooldown = random.randint(6000, 12000)
                print(f"[⏳] Cooling down for {cooldown/1000} seconds...\n")
                await page.wait_for_timeout(cooldown)

                print(f"[✓] Finished interaction with: {url}")
            except Exception as e:
                print(f"[✗] Error visiting {url}: {e}")

        await browser.close()

# 🚀 Run
asyncio.run(visit_links())
