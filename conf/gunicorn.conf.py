import multiprocessing
import asyncio


name = "clashleaders.com"
bind = "unix:/tmp/gunicorn.sock"
workers = multiprocessing.cpu_count()
threads = multiprocessing.cpu_count()
worker_connections = 10000
worker_class = "gevent"


def post_fork(server, worker):
    from gevent import monkey

    monkey.patch_all()
    asyncio.set_event_loop(asyncio.new_event_loop())
