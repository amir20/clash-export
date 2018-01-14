import logging
import os
from datetime import timedelta

import requests_cache
from flask import Flask, json
from flask_caching import Cache
from mongoengine import connect
from raven.contrib.flask import Sentry

app = Flask(__name__)
app.debug = os.getenv('DEBUG', False)
sentry = Sentry(app)
logging.basicConfig(level=logging.INFO)

# Cache settings
requests_cache.install_cache(expire_after=timedelta(seconds=10), backend='memory')
cache = Cache(app, config={'CACHE_TYPE': 'null' if app.debug else 'filesystem', 'CACHE_DIR': '/tmp'})

# Set connect to False for pre-forking to work
connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)

import clashleaders.views  # noqa


def manifest_path(file):
    SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
    manifest = os.path.join(SITE_ROOT, "static", "manifest.json")
    with open(manifest) as f:
        data = json.load(f)
    return data[file]


app.add_template_global(manifest_path, 'manifest_path')
