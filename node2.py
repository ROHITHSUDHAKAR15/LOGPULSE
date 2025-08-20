from log import generate_info_log, random_log_level, generate_registration_log, generate_warn_log, generate_error_log
from heartbeat import send_heartbeat
import threading
import time
import random
import json
import requests

FLUENTD_URL = "http://localhost:9880/log.input"

def main():
    node_id = "node_02"
    service_name = "Order"

    terminate = 0

    registration_log = generate_registration_log(node_id, service_name)
    requests.post(FLUENTD_URL, data=json.dumps(registration_log), headers={'Content-Type': 'application/json'})

    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(node_id, FLUENTD_URL))
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

    while True:
        log_level = random_log_level()
        log_message = f"Sample log message from {node_id}"
        match log_level:
            case "INFO":
                log = generate_info_log(node_id, log_level, service_name, log_message)
            case "WARN":
                log = generate_warn_log(node_id, log_level, service_name, log_message)
            case "ERROR":
                log = generate_error_log(node_id, log_level, service_name, log_message)
                terminate = 1
        time.sleep(1)
        requests.post(FLUENTD_URL, data=json.dumps(log), headers={'Content-Type': 'application/json'})
        if terminate == 1:
           break

if __name__ == "__main__":
    main()
