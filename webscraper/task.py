from redis import Redis
from rq import Queue
import subprocess

r = Redis(host="redis", port=6379)
q = Queue("default", connection=r)


def run_spider_task(spider_name: str):
    """Funkcija koja pokreće Scrapy spider kao subprocess"""
    print(f"Pokrećem spider: {spider_name}")
    subprocess.run(["scrapy", "crawl", spider_name])
