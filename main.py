# -*- coding: utf-8 -*-
import requests
import os
import re
import sys

def change_group_name_api():
    # --- ⚙️ GATHER CREDENTIALS FROM GITHUB SECRETS ---
    raw_cookie = os.environ.get("INSTA_COOKIE")
    thread_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    
    # Constructing the exact name pattern requested
    new_name = f"({target_name}) SAY P R V R daddy"

    if not raw_cookie or not thread_id:
        print("❌ FAILED: Missing Secrets (INSTA_COOKIE or TARGET_THREAD_ID)")
        return

    # Extract sessionid and csrftoken using Regex
    sid_match = re.search(r'sessionid=([^;]+)', raw_cookie)
    csrf_match = re.search(r'csrftoken=([^;]+)', raw_cookie)
    
    if not sid_match or not csrf_match:
        print("❌ FAILED: Cookie must contain sessionid and csrftoken.")
        return

    session_id = sid_match.group(1).strip()
    csrf_token = csrf_match.group(1).strip()

    # --- ⚙️ BROWSER HANDSHAKE HEADERS ---
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "X-CSRFToken": csrf_token,
        "X-IG-App-ID": "936619743392459", 
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"https://www.instagram.com/direct/t/{thread_id}/",
        "Cookie": f"sessionid={session_id}; csrftoken={csrf_token};",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # API Endpoint for setting the thread title
    url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/set_title/"
    payload = {"title": new_name}

    print(f"🚀 Sending API Request to Thread: {thread_id}...")
    print(f"📝 New Name: {new_name}")
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "ok":
                print(f"✅ SUCCESS: Group name changed to: {new_name}")
            else:
                print(f"⚠️ REJECTED: {result}")
        else:
            print(f"❌ FAILED: Status {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ REQUEST ERROR: {e}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    change_group_name_api()
