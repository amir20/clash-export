import multiprocessing
import os


name = "clashleaders.com"
bind = "unix:/tmp/gunicorn.sock"
workers = 2
worker_class = "sync"

reload = bool(os.getenv("DEBUG", False))
