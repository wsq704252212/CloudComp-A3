from elasticsearch import Elasticsearch, RequestsHttpConnection
import boto3
import json

# create es on aws before execution

host = 'search-photos-vxlnrbcnhsji3zk6gcylzym3pa.us-east-1.es.amazonaws.com'
region = 'us-east-1'
service = 'es'

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=("ycc", "YccWsq2024!"),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# type is dedeprecated in es 7.10
resp = es.indices.create(
    index="test",
    body={
        "mappings": {
            "properties": {
                "objectKey": { "type": "text" },
                "bucket": { "type": "text" },
                "createdTimestamp": { "type": "text" },
                "labels": { "type": "text" }
            }
        }
    },
)

print(resp)