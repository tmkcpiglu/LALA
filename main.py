# -*- coding: utf-8 -*-
import requests
import uuid
import os
import re
import sys
import time

def ignite():
    # --- ⚙️ GATHER SECRETS ---
    raw_cookie = os.environ.get("INSTA_COOKIE", "")
    thread_id = os.environ.get("TARGET_THREAD_ID", "").strip()
    BRANDING = "𝚂ᴀ𝚈 【﻿ＰＲＶ𝐑】 𝐃ᴀ𝐃𝐃𝐘 ~⭕"

    if not raw_cookie or not thread_id:
        print("❌ FAILED: Missing Secrets.")
        return

    sid_match = re.search(r'sessionid=([^;]+)', raw_cookie)
    session_id = sid_match.group(1).strip() if sid_match else raw_cookie

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-IG-App-ID": "936619743392459",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
    })
    session.cookies.set("sessionid", session_id, domain=".instagram.com")

    start_time = time.time()
    # 21000 seconds = 5 hours and 50 minutes (to finish before GitHub kills it at 6h)
    MAX_RUN_TIME = 21000 

    print(f"🚀 Guardian Deployment Active for 6 Hours.")
    print(f"🛡️  Monitoring Thread: {thread_id}")

    while (time.time() - start_time) < MAX_RUN_TIME:
        try:
            # 1. Monitor the current name
            resp = session.get(f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/")
            if resp.status_code == 200:
                current_name = resp.json().get("thread", {}).get("thread_title", "")
                
                if current_name != BRANDING:
                    print(f"\n🚨 BREACH: Name changed to '{current_name}'. Reverting...")
                    
                    # Fetch fresh CSRF for the strike
                    session.get("https://www.instagram.com/")
                    csrf = session.cookies.get("csrftoken", "")
                    
                    payload = {
                        "title": BRANDING,
                        "_csrftoken": csrf,
                        "_uuid": str(uuid.uuid4()),
                    }
                    strike = session.post(
                        f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/update_title/",
                        data=payload,
                        headers={"X-CSRFToken": csrf}
                    )
                    
                    if strike.status_code == 200:
                        print(f"✅ Re-Secured: {BRANDING}")
                    else:
                        print(f"❌ Revert Failed: {strike.status_code}")
                else:
                    # Log progress on one line to keep logs clean
                    sys.stdout.write(f"\r🛡️  Secure | Time Active: {int((time.time() - start_time)/60)}m")
                    sys.stdout.flush()
            
            elif resp.status_code == 401:
                print("\n❌ Session Expired.")
                break
                
        except Exception as e:
            print(f"\n⚠️ Blip: {e}")
            time.sleep(30) # Wait longer if there's a connection error

        time.sleep(15) # Check every 15 seconds

    print("\n⌛ 6-Hour Shift Complete. Shutting down for reboot.")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    ignite()
