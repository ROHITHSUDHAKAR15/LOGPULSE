# LogPulse

LogPulse is a simple, reproducible logging demo. It simulates a few services, sends their logs/heartbeats over HTTP to Kafka, processes them, writes to a search backend, and prints alerts.

## What you need
- Python 3.12+
- Kafka running on `localhost:9092`
- One search backend (pick one): Elasticsearch 8+ or OpenSearch 2+/3+
- Fluentd (HTTP input) using the provided `fluent.conf`

## Install (once)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start the basics
1) Kafka (macOS/Homebrew example)
```bash
brew install kafka
brew services start kafka
```
2) Search backend (choose one)
- OpenSearch (Homebrew):
  ```bash
  brew install opensearch
  brew services start opensearch
  ```
- Elasticsearch: use your preferred install. If HTTPS is on, keep the password and CA cert handy.
3) Fluentd (HTTP → Kafka)
```bash
sudo gem install fluentd fluent-plugin-kafka --no-document
fluentd -c fluent.conf
```
Fluentd listens at `http://localhost:9880/log.input`.

## Run the demo (4 terminals)
- Terminal A (processor):
```bash
python pub_sub_model.py nodes processed_logs alerts
```
- Terminal B (storage → search backend):
```bash
python log_storage.py processed_logs
```
- Terminal C (alerts):
```bash
python alert_system.py alerts
```
- Terminals D–F (simulated nodes):
```bash
python node1.py
python node2.py
python node3.py
```

## Search and clean up
- Search by level or type:
```bash
python search_es_storage.py ERROR
python search_es_storage.py REGISTRATION
```
- Delete all logs:
```bash
python delete_es_storage.py
```

## Optional config (env vars)
- Kafka: `KAFKA_BOOTSTRAP` (default `localhost:9092`)
- Elasticsearch: `ELASTIC_URL` (default `http://localhost:9200`), plus `ELASTIC_PASSWORD` and `ELASTIC_CA_CERT` if HTTPS
- OpenSearch: set `USE_OPENSEARCH=1` and `OPENSEARCH_URL` (e.g., `http://localhost:9200`)

## If something doesn’t work
- 9880 connection refused → start Fluentd and keep it running
- Kafka errors → start Kafka and ensure `localhost:9092`
- No search results → make sure nodes are running and storage consumer is started

## Files
- `node1.py`, `node2.py`, `node3.py` — simulated services
- `heartbeat.py`, `log.py` — helpers for heartbeats/logs
- `fluent.conf` — Fluentd config
- `pub_sub_model.py` — processing + heartbeat monitor
- `log_storage.py` — writes to Elasticsearch/OpenSearch
- `alert_system.py` — prints alerts
- `search_es_storage.py`, `delete_es_storage.py` — utilities
- `requirements.txt`

 
