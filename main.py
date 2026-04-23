# -*- coding: utf-8 -*-
from instagrapi import Client
import os
import sys
import re

def ignite():
    # --- ⚙️ GATHER SECRETS ---
    session_raw = os.environ.get("INSTA_COOKIE")
    thread_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    
    new_name = f"({target_name}) SAY P R V R daddy"

    if not session_raw or not thread_id:
        print("❌ Missing Secrets!")
        return

    # Clean the session_id from the full cookie string
    session_id = session_raw
    if "sessionid=" in session_raw:
        match = re.search(r'sessionid=([^;]+)', session_raw)
        if match:
            session_id = match.group(1).strip()

    cl = Client()
    
    try:
        print("🚀 Booting Instagrapi Engine...")
        # Login via Session ID
        cl.login_by_sessionid(session_id)
        print(f"✅ Logged in as: {cl.username}")

        # ⚡ THE NAME FLIP (Corrected Method Name)
        print(f"📝 Attempting to change thread {thread_id} title to: {new_name}")
        
        # In current instagrapi, it is direct_thread_edit_title
        success = cl.direct_thread_edit_title(thread_id, new_name)
        
        if success:
            print(f"🔥 SUCCESS: Group name is now: {new_name}")
        else:
            print("⚠️ Server accepted request but title didn't change (Check if you are a member).")

    except AttributeError:
        # Fallback for older/different versions of the library
        print("⚠️ 'direct_thread_edit_title' failed, trying legacy method...")
        try:
            cl.direct_thread_set_title(thread_id, new_name)
            print("🔥 SUCCESS via legacy method!")
        except Exception as e:
            print(f"❌ Both methods failed: {e}")
            
    except Exception as e:
        print(f"❌ STRIKE FAILED: {e}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    ignite()
