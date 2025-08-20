from kafka import KafkaConsumer
import json
import sys
import os

topic_sub = sys.argv[1]
consumer = KafkaConsumer(
    topic_sub,
    value_deserializer=lambda m: json.loads(m.decode('ascii')),
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP', 'localhost:9092')
)

for message in consumer:
    print(f"{message.value['log_level']}: {message.value['node_id']}, {message.value['log_id']}")
