import requests
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

def loading_animation(user_id):
    loading_url = 'https://api.line.me/v2/bot/chat/loading/start'
    channel_access_token = os.getenv("LINE_ACCESS_TOKEN")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}',        
    }
    data = {
        "chatId": user_id,
        "loadingSeconds": 5
    }

    try:
        requests.post(loading_url, headers=headers, json=data)
    except Exception as e:
        print("Loading API failed:", e)