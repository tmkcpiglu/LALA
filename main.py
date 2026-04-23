# -*- coding: utf-8 -*-
import requests, os, re, sys, uuid

def change_name(thread_id, name, headers):
    # Testing the V1 vs V2 endpoint logic
    url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/set_title/"
    payload = {
        "title": name,
        "client_context": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4())
    }
    return requests.post(url, data=payload, headers=headers)

def ignite():
    raw_cookie = os.environ.get("INSTA_COOKIE", "")
    thread_id = os.environ.get("TARGET_THREAD_ID", "").strip()
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    new_name = f"({target_name}) SAY P R V R daddy"

    sid = re.search(r'sessionid=([^;]+)', raw_cookie)
    csrf = re.search(r'csrftoken=([^;]+)', raw_cookie)
    
    if not sid or not csrf:
        print("❌ Cookie Format Error.")
        return

    s_id, c_token = sid.group(1).strip(), csrf.group(1).strip()

    headers = {
        "x-csrftoken": c_token,
        "x-ig-app-id": "936619743392459",
        "x-instagram-ajax": "1",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f"csrftoken={c_token}; sessionid={s_id};",
        "user-agent": "Mozilla/5.0 (iPhone; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
        "referer": "https://www.instagram.com/"
    }

    print(f"🚀 Refiring Strike on ID: {thread_id}")
    
    response = change_name(thread_id, new_name, headers)
    
    if response.status_code == 200:
        print(f"✅ SUCCESS: Name changed to {new_name}")
    elif response.status_code == 500:
        print("⚠️ Status 500 Detected. Retrying with Thread Mapping...")
        # If the ID is a long numeric, try stripping any potential formatting
        clean_id = re.sub(r'\D', '', thread_id)
        if clean_id != thread_id:
            response = change_name(clean_id, new_name, headers)
            if response.status_code == 200:
                print(f"✅ SUCCESS on Retry: Name changed.")
                return
        
        print("❌ Still 500. This ID is likely restricted or ghosted by Meta.")
        print("👉 ACTION: Open Group -> F12 -> Network -> Type something -> Find 'send_item' -> Copy 'thread_id' from Payload.")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text[:150]}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    ignite()
