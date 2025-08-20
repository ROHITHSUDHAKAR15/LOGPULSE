import time
import json
import requests

def send_heartbeat(node_id, url):
    while True:
        heartbeat_message = {
            "node_id": node_id,
            "message_type": "HEARTBEAT",
            "status": "UP",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        requests.post(url, data=json.dumps(heartbeat_message), headers={'Content-Type': 'application/json'})
        time.sleep(5) 
