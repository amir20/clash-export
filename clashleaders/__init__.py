import logging
import os

import bugsnag
from bugsnag.flask import handle_exceptions
from flask import Flask, json
from flask_caching import Cache
from mongoengine import connect

app = Flask(__name__)
app.debug = os.getenv('DEBUG', False)

bugsnag.configure(
    api_key=os.getenv('BUGSNAG_API_KEY'),
    project_root="/app",
    release_stage=os.getenv('STAGE', 'development'),
    notify_release_stages=["production"]
)
handle_exceptions(app)

logging.basicConfig(level=logging.INFO)

# Cache settings
cache = Cache(app, config={'CACHE_TYPE': 'null' if app.debug else 'filesystem', 'CACHE_DIR': '/tmp'})

# Set connect to False for pre-forking to work
connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)

import clashleaders.views  # noqa

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST_FILE = os.path.join(SITE_ROOT, "static", "manifest.json")


def manifest_path(file):
    with open(MANIFEST_FILE) as f:
        data = json.load(f)
    return data[file]


def inline_path(file):
    path = os.path.join(SITE_ROOT, "static", manifest_path(file))
    with open(path) as f:
        return f.read()


app.add_template_global(manifest_path, 'manifest_path')
app.add_template_global(inline_path, 'inline_path')
