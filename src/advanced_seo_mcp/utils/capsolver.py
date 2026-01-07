import requests
import time
import os
from typing import Optional

# Get API Key from environment variable
api_key = os.environ.get("CAPSOLVER_API_KEY")

def get_capsolver_token(site_url: str) -> Optional[str]:
    """
    Use CapSolver to solve the captcha and get a token
    
    Args:
        site_url: Site URL to query
        
    Returns:
        Verification token or None if failed
    """
    if not api_key:
        return None
    
    payload = {
        "clientKey": api_key,
        "task": {
            "type": 'AntiTurnstileTaskProxyLess',
            "websiteKey": "0x4AAAAAAAAzi9ITzSN9xKMi",  # site key of your target site: ahrefs.com,
            "websiteURL": site_url,
            "metadata": {
                "action": ""  # optional
            }
        }
    }
    try:
        res = requests.post("https://api.capsolver.com/createTask", json=payload, timeout=10)
        res.raise_for_status()
        resp = res.json()
        task_id = resp.get("taskId")
        if not task_id:
            return None
    
        while True:
            time.sleep(1)  # delay
            payload = {"clientKey": api_key, "taskId": task_id}
            res = requests.post("https://api.capsolver.com/getTaskResult", json=payload, timeout=10)
            resp = res.json()
            status = resp.get("status")
            if status == "ready":
                token = resp.get("solution", {}).get('token')
                return token
            if status == "failed" or resp.get("errorId"):
                return None
    except Exception as e:
        print(f"CapSolver Error: {e}")
        return None
