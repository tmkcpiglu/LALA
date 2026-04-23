# -*- coding: utf-8 -*-
import asyncio, os, sys, random, re, gc
from playwright.async_api import async_playwright

# --- ⚙️ V100 FORCE SETTINGS ---
AGENTS_PER_MACHINE = 2    
TABS_PER_AGENT = 2         
PULSE_DELAY = 100          # ⚡ Locked at 100ms as requested
STRIKE_CYCLE_SEC = 90      # ♻️ 90s Reset to prevent UI ghosting

async def apply_stealth_overdrive(page):
    """iPad Pro Hardware Masking & Tracker Block"""
    await page.add_init_script("""
        delete window.navigator.webdriver;
        Object.defineProperty(navigator, 'platform', { get: () => 'iPad' });
        Object.defineProperty(navigator, 'vendor', { get: () => 'Apple Computer, Inc.' });
        window.chrome = { runtime: {} };
    """)
    client = await page.context.new_cdp_session(page)
    await client.send("Network.setBlockedURLs", {
        "urls": ["*graph.instagram.com*", "*logging.instagram.com*", "*/logging/*", "*.facebook.com*"]
    })

async def run_tab(context, target_id, target_name):
    page = await context.new_page()
    try:
        await apply_stealth_overdrive(page)
        
        # ⚡ Navigate & Wait for UI Stability
        await page.goto(f"https://www.instagram.com/direct/t/{target_id}/", wait_until="commit", timeout=60000)
        await asyncio.sleep(10) # Added buffer for GitHub Runner lag
        
        # ⚡ FORCE-STRIKE JS ENGINE
        await page.evaluate("""
            ([tName, mDelay]) => {
                const frames = ["⭕", "🌀", "🔴", "💠", "🧿", "🔘"];
                let frameIndex = 0;
                window.strikeTimer = setInterval(() => {
                    // Aggressive Selector for iPad/Mobile UI
                    const box = document.querySelector('div[aria-label="Message"], div[role="textbox"], [contenteditable="true"]');
                    if (box) {
                        const emoji = frames[frameIndex % frames.length];
                        const pattern = `(${tName}) 𝚂ᴀ𝚈 【﻿ＰＲＶ𝐑】 𝐃ᴀ𝐃𝐃𝐘 ~${emoji}`;
                        const fullBlock = Array(20).fill(pattern).join('\\n') + `\\n⚡ ID: ${Math.random().toString(36).substring(7)}`;

                        box.focus();
                        // Re-trigger focus to wake up React handlers
                        box.dispatchEvent(new Event('focus', { bubbles: true }));
                        
                        document.execCommand('insertText', false, fullBlock);
                        box.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        const enter = new KeyboardEvent('keydown', { 
                            bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13 
                        });
                        box.dispatchEvent(enter);
                        
                        frameIndex++; 
                        // DOM Purge to keep speed high
                        setTimeout(() => { if(box.innerText.length > 0) box.innerHTML = ""; }, 5);
                    }
                }, mDelay);
            }
        """, [target_name, PULSE_DELAY])
        
        await asyncio.sleep(STRIKE_CYCLE_SEC)
    except: pass
    finally: await page.close()

async def run_agent(agent_id, cookie, target_id, target_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            "--no-sandbox", 
            "--disable-dev-shm-usage", 
            "--js-flags='--max-old-space-size=1024'"
        ])
        
        while True: 
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
                viewport={'width': 1024, 'height': 1366},
                is_mobile=True, has_touch=True
            )
            
            sid_match = re.search(r'sessionid=([^;]+)', cookie)
            sid = sid_match.group(1) if sid_match else cookie
            await context.add_cookies([{'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com', 'path': '/'}])
            
            tabs = [run_tab(context, target_id, target_name) for i in range(TABS_PER_AGENT)]
            await asyncio.gather(*tabs)
            
            await context.close()
            gc.collect()
            print(f"♻️ [Agent {agent_id}] Speed Purge Complete.")

async def main():
    cookie, t_id, t_name = os.environ.get("INSTA_COOKIE"), os.environ.get("TARGET_THREAD_ID"), os.environ.get("TARGET_NAME", "TARGET")
    if not cookie or not t_id: return
    agents = [run_agent(i + 1, cookie, t_id, t_name) for i in range(AGENTS_PER_MACHINE)]
    await asyncio.gather(*agents)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(main())
