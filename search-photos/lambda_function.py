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
        # inputText=json.loads(event['body'])['query']
        inputText='Show me some pictures of cats'
    )

    print(response)

    keywordOne = response['slots']['KeywordOne']
    keywordTwo = response['slots']['KeywordTwo']
    keywords = [keywordOne] if keywordTwo is None else [keywordOne, keywordTwo]

    # esaccount = ('ycc', 'YccWsq2024!')

    # query = {
    #     "query": {
    #         "function_score": {
    #             "query": {
    #                 "match": {"labels": keywords}
    #             },
    #             "functions": [
    #                 {
    #                     "random_score": {}
    #                 }
    #             ],
    #             "score_mode": "sum"
    #         }
    #     }
    # }

    # url = 'https://search-photos-vxlnrbcnhsji3zk6gcylzym3pa.us-east-1.es.amazonaws.com/photos/_search'
    # response = requests.get(url, auth=esaccount, json=query)
    # data = json.loads(response.content.decode())

    # print(data)

    # es = Elasticsearch('https://search-photos-vxlnrbcnhsji3zk6gcylzym3pa.us-east-1.es.amazonaws.com')
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

    response = s.execute()

    results = [hit for hit in response]

    print(results)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'keywords': keywords,
        })
    }
