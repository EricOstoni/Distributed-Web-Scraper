import boto3


dynamodb = boto3.client("dynamodb",
                           endpoint_url="http://localhost:8000", 
                           region_name="test", 
                           aws_access_key_id = "test",
                           aws_secret_access_key = "test") 

paginator = dynamodb.get_paginator("list_tables")

page_iterator = paginator.paginate(Limit=10)

print("Here are the DynamoDB tables in your local database:")

table_names = []



for page in page_iterator:
    for table_name in page.get("TableNames", []):
        print(f"- {table_name}")
        table_names.append(table_name)

if not table_names:
    print("There are no tables in your local database.")
else : 
    print(f"\nFound {len(table_names)} tables.")


