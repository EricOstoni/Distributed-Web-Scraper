# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
from botocore.exceptions import ClientError


class WebscraperPipeline:
    def process_item(self, item, spider):
        return item
    
    
#TODO izmjeniti ime tablice i mozda napraviti .env file

class DynamodbPipeline: 
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb" , region_name="croatia") 
        self.table = self.dynamodb.Table("table") 

    def process_item(self, item, spider): 
        try: 
            self.table.put_item(Item={
                "name" : item.get("name", ""),
                "price": item.get("price", "")
            })
        except ClientError as e:
            spider.logger.error(f"Error saveing item to database: {e.response['Error']['Message']}")
        return item
    
    