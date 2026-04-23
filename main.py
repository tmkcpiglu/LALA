# -*- coding: utf-8 -*-
import requests
import os
import re
import sys

def change_group_name_api():
    # --- ⚙️ GATHER CREDENTIALS ---
    raw_cookie = os.environ.get("INSTA_COOKIE", "")
    thread_id = os.environ.get("TARGET_THREAD_ID", "")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    
    new_name = f"({target_name}) SAY P R V R daddy"

    if not raw_cookie or not thread_id:
        print("❌ FAILED: Missing INSTA_COOKIE or TARGET_THREAD_ID in Secrets.")
        return

    # Extract sessionid and csrftoken with cleaner logic
    sid = re.search(r'sessionid=([^;]+)', raw_cookie)
    csrf = re.search(r'csrftoken=([^;]+)', raw_cookie)
    
    if not sid or not csrf:
        print("❌ FAILED: sessionid or csrftoken not found in the cookie string.")
        print("Ensure you copied the FULL cookie from the 'Request Headers' in Chrome.")
        return

    s_id = sid.group(1).strip()
    c_token = csrf.group(1).strip()

    # --- ⚙️ THE "FORCE" HEADERS ---
    # We add more headers to perfectly mimic a logged-in mobile session
    headers = {
        "authority": "www.instagram.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f"csrftoken={c_token}; sessionid={s_id};",
        "origin": "https://www.instagram.com",
        "referer": f"https://www.instagram.com/direct/t/{thread_id}/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (iPhone; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "x-csrftoken": c_token,
        "x-ig-app-id": "936619743392459",
        "x-instagram-ajax": "1",
        "x-requested-with": "XMLHttpRequest"
    }

    url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/set_title/"
    payload = {"title": new_name}

    print(f"🚀 Igniting API Strike on Thread: {thread_id}")
    
    try:
        # Using a Session object to handle cookies properly
        session = requests.Session()
        response = session.post(url, data=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "ok":
                print(f"✅ SUCCESS: Group name is now: {new_name}")
            else:
                print(f"⚠️ REJECTED BY META: {result}")
        elif response.status_code == 404:
            print("❌ ERROR 404: Page Not Found.")
            print("POSSIBLE CAUSES:")
            print("1. Your TARGET_THREAD_ID is wrong.")
            print("2. Your sessionid/csrftoken are expired or invalid.")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text[:200]}")

    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    change_group_name_api()
