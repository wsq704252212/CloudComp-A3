import json
import boto3
import requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

def lambda_handler(event, context):
    client = boto3.client('lex-runtime')

    print(event)

    response = client.post_text(
        botName='PhotoSearch',
        botAlias='$LATEST',
        userId='default',
        inputText=event.get('queryStringParameters', {}).get('q')
    )

    print(response)

    keywordOne = response['slots']['KeywordOne']
    keywordTwo = response['slots']['KeywordTwo']

    es = Elasticsearch(
        ["https://search-photos-vxlnrbcnhsji3zk6gcylzym3pa.us-east-1.es.amazonaws.com"],
        http_auth=("ycc", "YccWsq2024!")
    )

    s = Search(using=es, index="photos").query(
        "bool",
        must=(
            [{"match": {"labels": keywordOne}}]
            if keywordTwo is None
            else [{"match": {"labels": keywordOne}}, {"match": {"labels": keywordTwo}}]
        )
    )
    # s = Search(using=es, index="photos").query("match_all")

    response = s.execute()

    photoName = response[0].objectKey
    photoUrl = f"https://cirf-could-computing-photos.s3.amazonaws.com/{photoName}"

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'photoUrl': photoUrl,
            'photoName': photoName
        })
    }
