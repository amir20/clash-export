import multiprocessing

name = "clashleaders.com"
bind = "unix:/tmp/gunicorn.sock"
workers = multiprocessing.cpu_count() + 1
worker_connections = 10000
worker_class = "sync"
