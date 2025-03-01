import boto3
import os
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource(  'dynamodb',
            endpoint_url=os.getenv("DYNAMODB_ENDPOINT"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")) 

table = dynamodb.Table("Products") 
response = table.scan()
for item in response['Items']:
    print(item)