import json
import boto3
import requests

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

    print(keywords)


    esaccount = ('ycc', 'YccWsq2024!')

    query = {
        "query": {
            "function_score": {
                "query": {
                    "match": {"labels": keywords}
                },
                "functions": [
                    {
                        "random_score": {}
                    }
                ],
                "score_mode": "sum"
            }
        }
    }

    url = 'https://search-photos-vxlnrbcnhsji3zk6gcylzym3pa.us-east-1.es.amazonaws.com/photos/_search'
    response = requests.get(url, auth=esaccount, json=query)
    data = json.loads(response.content.decode())

    print(data)


    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'keywords': keywords,
        })
    }