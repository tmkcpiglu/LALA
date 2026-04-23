# -*- coding: utf-8 -*-
from instagrapi import Client
import os
import sys
import re

def ignite():
    session_raw = os.environ.get("INSTA_COOKIE")
    thread_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    
    # Exact pattern: (target) SAY P R V R daddy
    new_name = f"({target_name}) SAY P R V R daddy"

    if not session_raw or not thread_id:
        print("❌ Missing Secrets!")
        return

    # Extract session_id for clean login
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

        # ⚡ THE MULTI-STRIKE LOGIC
        # We include 'direct_thread_update_title' from your snippet
        methods = [
            'direct_thread_update_title', # Your newest method
            'direct_thread_edit_name',    # Common mobile method
            'direct_thread_edit_title',   # Common web method
            'direct_thread_set_title'     # Legacy method
        ]

        success = False
        for method_name in methods:
            if hasattr(cl, method_name):
                print(f"🔄 Trying method: {method_name}...")
                try:
                    method = getattr(cl, method_name)
                    # Instagrapi methods return the thread object or True on success
                    if method(thread_id, new_name):
                        print(f"🔥 SUCCESS: Group name flipped using {method_name}!")
                        success = True
                        break
                except Exception as e:
                    print(f"⚠️ {method_name} failed: {e}")
        
        if not success:
            print("❌ All methods failed. Your Thread ID might be invalid for this account.")

    except Exception as e:
        print(f"❌ LOGIN ERROR: {e}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    ignite()
