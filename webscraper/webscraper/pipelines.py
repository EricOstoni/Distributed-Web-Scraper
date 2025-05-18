import boto3
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


class DynamoDBPipeline:
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=os.getenv("DYNAMODB_ENDPOINT"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        self.table_name = "Products"

        existing_tables = self.dynamodb.meta.client.list_tables()["TableNames"]
        if self.table_name not in existing_tables:
            self.table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            self.table.wait_until_exists()
        else:
            self.table = self.dynamodb.Table(self.table_name)

    def process_item(self, item, spider):
        item["id"] = str(uuid.uuid4())
        category_map = {
            "iphone_spider": "iPhone",
            "mac_spider": "Mac",
            "macbook_spider": "MacBook",
            "ipad_spider": "Ipad",
            "iwatch_spider": "Apple Watch",
        }
        item["category"] = category_map.get(spider.name, "bo")
        self.table.put_item(Item=dict(item))
        return item
