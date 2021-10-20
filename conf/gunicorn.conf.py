import multiprocessing
import os


name = "clashleaders.com"
bind = "unix:/tmp/gunicorn.sock"
workers = 2
worker_class = "sync"
timeout = 300

reload = bool(os.getenv("DEBUG", False))
