# -*- coding: utf-8 -*-
from instagrapi import Client
import os
import sys

def ignite():
    # --- ⚙️ GATHER SECRETS ---
    session_id = os.environ.get("INSTA_COOKIE") # We will extract just the SID
    thread_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    
    new_name = f"({target_name}) SAY P R V R daddy"

    if not session_id or not thread_id:
        print("❌ Missing Secrets!")
        return

    # Clean the session_id (in case you pasted the whole cookie)
    if "sessionid=" in session_id:
        import re
        match = re.search(r'sessionid=([^;]+)', session_id)
        if match:
            session_id = match.group(1).strip()

    cl = Client()
    
    try:
        print("🚀 Booting Instagrapi Engine...")
        # Login via Session ID (Bypasses 2FA and Login alerts)
        cl.login_by_sessionid(session_id)
        print(f"✅ Logged in as: {cl.username}")

        # ⚡ THE NAME FLIP
        # Instagrapi uses the internal 'direct_thread_set_title' call
        success = cl.direct_thread_set_title(thread_id, new_name)
        
        if success:
            print(f"🔥 SUCCESS: Group name is now: {new_name}")
        else:
            print("⚠️ Request sent but server didn't confirm change.")

    except Exception as e:
        print(f"❌ STRIKE FAILED: {e}")
        print("💡 Hint: If it says 'Thread not found', double check your TARGET_THREAD_ID.")

if __name__ == "__main__":
    # Ensure UTF-8 for the special characters in the name
    sys.stdout.reconfigure(encoding='utf-8')
    ignite()
