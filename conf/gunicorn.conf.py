import multiprocessing


name = "clashleaders.com"
bind = "unix:/tmp/gunicorn.sock"
workers = multiprocessing.cpu_count()
worker_class = "sync"


def post_fork(server, worker):
    from gevent import monkey

    monkey.patch_all()
