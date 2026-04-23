# -*- coding: utf-8 -*-
from instagrapi import Client
import os
import sys
import re

def ignite():
    session_raw = os.environ.get("INSTA_COOKIE")
    thread_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    
    new_name = f"({target_name}) SAY P R V R daddy"

    if not session_raw or not thread_id:
        print("❌ Missing Secrets!")
        return

    # Extract session_id
    session_id = session_raw
    if "sessionid=" in session_raw:
        match = re.search(r'sessionid=([^;]+)', session_raw)
        if match:
            session_id = match.group(1).strip()

    cl = Client()
    
    try:
        print("🚀 Booting Instagrapi Engine...")
        cl.login_by_sessionid(session_id)
        print(f"✅ Logged in as: {cl.username}")
        print(f"📝 Target Thread: {thread_id}")

        # ⚡ THE MULTI-STRIKE LOGIC
        # We try every known method name in the instagrapi library
        methods = [
            'direct_thread_edit_name',  # Current most common
            'direct_thread_edit_title', # Alternative
            'direct_thread_set_name',   # Legacy 1
            'direct_thread_set_title'   # Legacy 2
        ]

        success = False
        for method_name in methods:
            if hasattr(cl, method_name):
                print(f"🔄 Trying method: {method_name}...")
                try:
                    method = getattr(cl, method_name)
                    if method(thread_id, new_name):
                        print(f"🔥 SUCCESS: Group name flipped using {method_name}!")
                        success = True
                        break
                except Exception as e:
                    print(f"⚠️ {method_name} failed: {e}")
        
        if not success:
            print("❌ All library methods failed. Check if your account is still in the group.")

    except Exception as e:
        print(f"❌ LOGIN OR SYSTEM ERROR: {e}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    ignite()
