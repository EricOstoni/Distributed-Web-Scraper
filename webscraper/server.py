from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
from dotenv import load_dotenv


load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT")
TABLE_NAME = os.getenv("TABLE_NAME")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=DYNAMODB_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

table = dynamodb.Table(TABLE_NAME)


@app.get("/products")
def get_products():
    response = table.scan()
    items = response.get("Items", [])
    return items
