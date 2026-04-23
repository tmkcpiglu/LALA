# -*- coding: utf-8 -*-
import requests, os, re, sys, uuid

def change_group_name_api():
    raw_cookie = os.environ.get("INSTA_COOKIE", "")
    thread_id = os.environ.get("TARGET_THREAD_ID", "")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    new_name = f"({target_name}) SAY P R V R daddy"

    if not raw_cookie or not thread_id:
        print("❌ Missing Secrets.")
        return

    # Extracting session essentials
    sid = re.search(r'sessionid=([^;]+)', raw_cookie)
    csrf = re.search(r'csrftoken=([^;]+)', raw_cookie)
    if not sid or not csrf:
        print("❌ Cookie Error: sessionid or csrftoken missing.")
        return

    s_id, c_token = sid.group(1).strip(), csrf.group(1).strip()
    
    # Generate a unique client context (prevents 500 errors)
    client_context = str(uuid.uuid4())

    headers = {
        "x-csrftoken": c_token,
        "x-ig-app-id": "936619743392459",
        "x-instagram-ajax": "1",
        "x-requested-with": "XMLHttpRequest",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f"csrftoken={c_token}; sessionid={s_id};",
        "user-agent": "Mozilla/5.0 (iPhone; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
        "referer": f"https://www.instagram.com/direct/t/{thread_id}/"
    }

    # The "Universal Payload" - matches the exact format Meta expects
    url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/set_title/"
    payload = {
        "title": new_name,
        "client_context": client_context
    }

    print(f"🚀 Refiring API Strike on Thread: {thread_id}")
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ SUCCESS: Group name is now: {new_name}")
        elif response.status_code == 500:
            print("❌ STILL Status 500: Instagram is rejecting the Thread ID format.")
            print("💡 FIX: Go to the group on your browser and double-check the ID in the URL.")
        else:
            print(f"❌ FAILED: {response.status_code} - {response.text[:100]}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    change_group_name_api()
