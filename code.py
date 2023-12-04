#just import the libraries such as json, boto3 which can be used as the lambda function code that allows only the json verified files
import json
import boto3

def lambda_handler(event, context):
    # now this will do check the event whether it was in S3 Record or not
    if 'Records' in event and len(event['Records']) > 0:
        for record in event['Records']:
            # Now we have extracted the S3 bucket and the key information
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            # Now lets do read the content of the s3 object
            s3_client = boto3.client('s3')
            response = s3_client.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read().decode('utf-8')

            # We are implementing the lambda function over the api gateway so then we need to do make the content was in JSON format 
            data = json.loads(content)

            # now do insert the data into DynamoDB
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('YourDynamoDBTableName')  #  here replace with your DynamoDB table name

            # here is see the 'id' is the primary key in DynamoDB
            item = {'id': data['id'], 'other_attribute': data['other_attribute']}
            
            # Now do insert the item into DynamoDB
            table.put_item(Item=item)

            print(f"Inserted data into DynamoDB: {item}")

    return {
        'statusCode': 200,
        'body': json.dumps('Data insertion successful')
    }
