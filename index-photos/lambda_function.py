import boto3
import json
import requests

esaccount = ("ycc","YccWsq2024!")

def lambda_handler(event, context):
    # TODO implement
    for record in event['Records']:
        bucketName = record['s3']['bucket']['name']
        objKey = record['s3']['object']['key']

        labels = getDetectLabels(bucketName, objKey) + getCustomLabels(bucketName, objKey)
        esObj = {
            "objectKey": objKey,
            "bucket": bucketName,
            "createdTimestamp": record["eventTime"],
            "labels": labels
        }
        jsonObj = json.dumps(esObj)
        print(jsonObj)
        
        url = "https://search-photos-vxlnrbcnhsji3zk6gcylzym3pa.us-east-1.es.amazonaws.com/photos/_doc"
        response = requests.post(url, auth=esaccount, data=jsonObj, headers={'Content-Type': 'application/json'})
        print(json.loads(response.text))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from index-photos!')
    }

def getDetectLabels(bucketName, objKey):
    rekognition_client = boto3.client('rekognition', region_name='us-east-1')

    # Call Rekognition to detect labels in the image
    response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': objKey,
            }
        },
        MaxLabels=10,  # Maximum number of labels to return
        MinConfidence=70  # Minimum confidence level for detected labels
    )

    # Print the detected labels
    #print('Detected labels:')
    labels = []
    for label in response['Labels']:
    #    print(f'{label["Name"]} - {label["Confidence"]:.2f}%') 
        labels.append(label["Name"])

    return labels

def getCustomLabels(bucketName, Objkey):
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    response = s3_client.head_object(Bucket=bucketName, Key=Objkey)
    header = response['ResponseMetadata']['HTTPHeaders']
    labelsStr = header.get('x-amz-meta-customlabels', [])
    labels = labelsStr.split(",")
    print(labels)
    return labels
