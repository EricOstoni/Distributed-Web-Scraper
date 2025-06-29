from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import boto3, os, redis, json
from dotenv import load_dotenv
from task import q, run_spider_task
from fuzzywuzzy import fuzz

load_dotenv()

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://34.102.218.251"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=os.getenv("DYNAMODB_ENDPOINT"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)
table = dynamodb.Table(os.getenv("TABLE_NAME"))
r = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.get("/")
def read_root():
    return {"message": "Backend API is running."}


def guess_category_from_input(keyword: str) -> str | None:
    keyword = keyword.lower()
    categories = {
        "iphone": "iPhone",
        "ipad": "Ipad",
        "macbook": "MacBook",
        "mac": "Mac",
        "watch": "Apple Watch",
        "iwatch": "Apple Watch",
    }

    for key in categories:
        if key in keyword:
            return categories[key]

    best_match = max(categories.keys(), key=lambda k: fuzz.partial_ratio(k, keyword))
    if fuzz.partial_ratio(best_match, keyword) >= 60:
        return categories[best_match]
    return None


@app.get("/products")
def get_products(category: str = Query(None)):
    if category:
        matched_category = guess_category_from_input(category)
        if not matched_category:
            return JSONResponse(
                status_code=400, content={"error": "Nepoznata kategorija."}
            )

        cache_key = f"products:{matched_category.lower()}"
        cache = r.get(cache_key)
        if cache:
            return JSONResponse(content=json.loads(cache))
        else:
            items = table.scan().get("Items", [])
            filtered = [
                item
                for item in items
                if item.get("category", "").lower() == matched_category.lower()
            ]
            r.set(cache_key, json.dumps(filtered), ex=300)
            return JSONResponse(content=filtered)

    # fallback bez kategorije
    cache = r.get("products")
    if cache:
        return JSONResponse(content=json.loads(cache))
    else:
        items = table.scan().get("Items", [])
        r.set("products", json.dumps(items), ex=300)
        return JSONResponse(content=items)


@app.post("/run-spider/{spider_name}")
async def run_spider(spider_name: str, background_tasks: BackgroundTasks):
    job = q.enqueue(run_spider_task, spider_name)
    return {"message": f"Task za {spider_name} enqueue-an", "job_id": job.id}


def extract_categories(keyword: str):
    keyword = keyword.lower()
    categories = []
    mapping = {
        "iphone": "iphone_spider",
        "ipad": "ipad_spider",
        "macbook": "macbook_spider",
        "mac": "mac_spider",
        "watch": "iwatch_spider",
        "iwatch": "iwatch_spider",
    }

    for key, spider in mapping.items():
        if key in keyword and spider not in categories:
            categories.append(spider)

    if not categories:
        best_match = max(mapping.keys(), key=lambda k: fuzz.partial_ratio(k, keyword))
        if fuzz.partial_ratio(best_match, keyword) >= 60:
            categories.append(mapping[best_match])

    return categories


@app.post("/scraper")
async def auto_run_multiple_spiders(keyword: str = Query(...)):
    spiders = extract_categories(keyword)

    if not spiders:
        return JSONResponse(status_code=400, content={"error": "Nepoznata kategorija."})

    job_ids = []
    for spider in spiders:
        job = q.enqueue(run_spider_task, spider)
        job_ids.append(job.id)

    return {
        "message": f"Pokrenuti spideri za: {', '.join(spiders)}",
        "job_ids": job_ids,
    }
