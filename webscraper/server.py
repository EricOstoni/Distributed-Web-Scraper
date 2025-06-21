from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
from dotenv import load_dotenv
import redis
import json


load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT")
TABLE_NAME = os.getenv("TABLE_NAME")

# app = FastAPI()
app = FastAPI(root_path="/api")


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],
    # allow_origins=["*"],
    allow_origins=["http://34.102.218.251"],
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

r = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.get("/")
def read_root():
    return {"message": "Backend API is running."}


@app.get("/products")
def get_products():
    cache = r.get("products")
    if cache:
        print("imam cache")
        return JSONResponse(content=json.loads(cache))
    else:
        print("nemam cache")
        response = table.scan()
        items = response.get("Items", [])

        r.set("products", json.dumps(items), ex=300)

        return JSONResponse(content=items)
