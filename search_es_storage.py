from elasticsearch import Elasticsearch
import sys
import os

check = sys.argv[1]

use_opensearch = os.getenv("USE_OPENSEARCH", "0") == "1" or os.getenv("OPENSEARCH_URL") is not None

if use_opensearch:
    from opensearchpy import OpenSearch
    opensearch_url = os.getenv("OPENSEARCH_URL", os.getenv("ELASTIC_URL", "http://localhost:9200"))
    os_username = os.getenv("OPENSEARCH_USERNAME")
    os_password = os.getenv("OPENSEARCH_PASSWORD")
    os_ca_path = os.getenv("OPENSEARCH_CA_CERT")
    if opensearch_url.startswith("https://"):
        es = OpenSearch(
            hosts=[opensearch_url],
            http_auth=(os_username, os_password) if os_username and os_password else None,
            use_ssl=True,
            verify_certs=True if os_ca_path else False,
            ca_certs=os.path.expanduser(os_ca_path) if os_ca_path else None,
        )
    else:
        es = OpenSearch(hosts=[opensearch_url])
else:
    elastic_url = os.getenv("ELASTIC_URL", "http://localhost:9200")
    elastic_password = os.getenv("ELASTIC_PASSWORD")
    ca_certs_path = os.getenv("ELASTIC_CA_CERT")
    if elastic_url.startswith("https://"):
        ca_path = os.path.expanduser(ca_certs_path) if ca_certs_path else None
        es = Elasticsearch(
            elastic_url,
            ca_certs=ca_path,
            basic_auth=("elastic", elastic_password) if elastic_password else None,
        )
    else:
        es = Elasticsearch(elastic_url)

if check == "REGISTRATION" or check == "HEARTBEAT":
    query = {
        "query": {
            "match": {
                "message_type": check
            }
        }
    }
else:
    query = {
        "query": {
            "match": {
                "log_level": check
            }
        }
    }

try:
    response = es.search(index="logs", body=query)
except TypeError:
    # OpenSearch client v2 uses 'body', v1 uses 'body', ES 8 Python client may use 'query' arg
    response = es.search(index="logs", body=query)

print(f"Search results for {check}:")
for hit in response['hits']['hits']:
    print(hit['_source'])
