import requests
import json

BASE_URL = "http://localhost:8000"
EMAIL = "test_user_unique@example.com"
PASSWORD = "password123"

def test_ai_storage():
    session = requests.Session()
    
    # 1. Login
    print("1. Logging in...")
    resp = session.post(f"{BASE_URL}/login", json={"email": EMAIL, "password": PASSWORD})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    
    token_data = resp.json()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    
    # 2. Call /ask with a title (to create a new chat)
    print("\n2. Calling /ask with 'title' to create new chat...")
    ai_payload = {
        "message": "What is the capital of France?",
        "title": "Geography Chat"
    }
    resp = session.post(f"{BASE_URL}/ask", json=ai_payload, headers=headers)
    if resp.status_code != 200:
        print(f"AI request failed (Status {resp.status_code}): {resp.text}")
        return
    
    try:
        ai_data = resp.json()
    except Exception as e:
        print(f"FAILED to decode JSON: {e}")
        print(f"Raw Response: {resp.text}")
        return
    chat_id = ai_data.get("chat_id")
    print(f"AI Response: {ai_data['response']}")
    print(f"Stored in Chat ID: {chat_id}")
    
    if not chat_id:
        print("FAILURE: chat_id not returned in AI response.")
        return

    # 3. Verify chat history contains the new chat
    print("\n3. Verifying chat history (GET /chats/)...")
    resp = session.get(f"{BASE_URL}/chats/", headers=headers)
    history = resp.json()
    found_chat = next((c for c in history if c["id"] == chat_id), None)
    
    if found_chat and found_chat["title"] == "Geography Chat":
        print(f"SUCCESS: Chat 'Geography Chat' found in history.")
    else:
        print(f"FAILURE: Chat not found in history. History: {history}")
        return

    # 4. Verify messages are stored
    print(f"\n4. Verifying messages in chat {chat_id} (GET /chats/{chat_id})...")
    resp = session.get(f"{BASE_URL}/chats/{chat_id}", headers=headers)
    full_chat = resp.json()
    messages = full_chat.get("messages", [])
    
    print(f"Found {len(messages)} messages:")
    for m in messages:
        print(f"  [{m['role']}]: {m['content'][:50]}...")
    
    has_user = any(m["role"] == "user" for m in messages)
    has_assistant = any(m["role"] == "assistant" for m in messages)
    
    if has_user and has_assistant:
        print("SUCCESS: Both user message and AI response are stored.")
    else:
        print("FAILURE: Missing messages in storage.")

if __name__ == "__main__":
    test_ai_storage()
