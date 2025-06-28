from redis import Redis
from rq import Worker, Queue


listen = ["default"]
redis_conn = Redis(host="redis", port=6379)

if __name__ == "__main__":
    print("✅ Pokrećem worker...")
    queue_list = [Queue(name, connection=redis_conn) for name in listen]
    worker = Worker(queues=queue_list, connection=redis_conn)
    worker.work(with_scheduler=True)
