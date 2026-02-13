import requests
import json
import sys

BASE_URL = "http://localhost:8000"
EMAIL = "test_user_unique@example.com"
PASSWORD = "password123"

def run_test():
    session = requests.Session()
    
    # 1. Signup/Login
    print(f"1. Authenticating as {EMAIL}...")
    try:
        # Try login first
        print("Attempting login...")
        resp = session.post(f"{BASE_URL}/login", json={"email": EMAIL, "password": PASSWORD})
        if resp.status_code != 200:
            # Try signup
            print("Login failed, trying signup...")
            signup_resp = session.post(f"{BASE_URL}/signup", json={"email": EMAIL, "password": PASSWORD})
            if signup_resp.status_code not in [200, 201]:
                 # Maybe user already exists?
                 print(f"Signup response: {signup_resp.status_code} {signup_resp.text}")

            # Always try logging in again after signup attempt
            print("Logging in after signup attempt...")
            resp = session.post(f"{BASE_URL}/login", json={"email": EMAIL, "password": PASSWORD})
            if resp.status_code != 200:
                print(f"FATAL: Could not authenticate. {resp.text}")
                return

        token_data = resp.json()
        access_token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        print("Authentication successful.")

        # 2. Create Chat
        print("\n2. Creating new chat...")
        resp = requests.post(
            f"{BASE_URL}/chats/", 
            json={"title": "Test Chat"}, 
            headers=headers
        )
        if resp.status_code != 200:
            print(f"FATAL: Create chat failed: {resp.text}")
            return
        
        chat_data = resp.json()
        chat_id = chat_data["id"]
        print(f"Chat created. ID: {chat_id}")

        # 3. Add Message
        print(f"\n3. Adding message to chat {chat_id}...")
        msg_payload = {"role": "user", "content": "Hello from test script"}
        resp = requests.post(
            f"{BASE_URL}/chats/{chat_id}/messages",
            json=msg_payload,
            headers=headers
        )
        if resp.status_code != 200:
            print(f"FATAL: Add message failed: {resp.text}")
            return
        
        msg_data = resp.json()
        print(f"Message added. ID: {msg_data['id']}")

        # 4. Verify Message Storage (Get Chat)
        print(f"\n4. Verifying message storage (GET /chats/{chat_id})...")
        resp = requests.get(f"{BASE_URL}/chats/{chat_id}", headers=headers)
        if resp.status_code != 200:
            print(f"FATAL: Get chat failed: {resp.text}")
            return
        
        full_chat = resp.json()
        messages = full_chat.get("messages", [])
        print(f"Retrieved {len(messages)} messages.")
        if len(messages) > 0 and messages[-1]["content"] == "Hello from test script":
            print("SUCCESS: Message content verified.")
        else:
            print(f"FAILURE: Message content mismatch or empty. contents: {messages}")

        # 5. Verify History (Get Chats)
        print("\n5. Verifying history listing (GET /chats/)...")
        resp = requests.get(f"{BASE_URL}/chats/", headers=headers)
        history = resp.json()
        print(f"Retrieved {len(history)} chats in history.")
        
        found = any(c["id"] == chat_id for c in history)
        if found:
            print("SUCCESS: Chat found in history.")
        else:
            print("FAILURE: Chat NOT found in history.")

    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    try:
        run_test()
    except ImportError:
        print("requests module not found. Please install it: pip install requests")
