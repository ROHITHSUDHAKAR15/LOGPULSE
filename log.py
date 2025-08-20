import time
import random
import uuid
import datetime

def random_log_level():
    levels = ["INFO", "WARN", "ERROR"]
    weights = [0.8, 0.15, 0.05]
    return random.choices(levels, weights, k=1)[0]

def generate_info_log(node_id, log_level, service_name, message):
    log = {
        "log_id": f"{node_id}_{uuid.uuid4()}",
        "node_id": node_id,
        "log_level": log_level,
        "message": message,
        "message_type": "LOG",
        "service_name": service_name,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return log

def generate_warn_log(node_id, log_level, service_name, message):
    response_time_ms = random.randint(100, 1000)
    threshold_limit_ms = random.randint(300, 800)

    log = {
        "log_id": f"{node_id}_{uuid.uuid4()}",
        "node_id": node_id,
        "log_level": log_level,
        "message": message,
        "message_type": "LOG",
        "response_time_ms": response_time_ms,
        "threshold_limit_ms": threshold_limit_ms,
        "service_name": service_name,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return log

def generate_error_log(node_id, log_level, service_name, message):
    log = {
        "log_id": f"{node_id}_{uuid.uuid4()}",
        "node_id": node_id,
        "log_level": log_level,
        "message": message,
        "message_type": "LOG",
        "error_details": {
            "error_code": random.randint(20, 100),
            "error_message": "some bs"
        },
        "service_name": service_name,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return log

def generate_registration_log(node_id, service_name):
    registration_log = {
        "node_id": node_id,
        "message_type": "REGISTRATION",
        "service_name": service_name,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return registration_log

def generate_microservice_log(log):
    converted_log = {
        'message_type' : 'REGISTRATION',
        'node_id' : log['node_id'],
        'service_name' : log['service_name'],
        'timestamp' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if log['message_type'] == "REGISTRATION":
        converted_log['status'] = "UP"
    if log['message_type'] == "LOG":
        converted_log['status'] = "DOWN"

    return converted_log


