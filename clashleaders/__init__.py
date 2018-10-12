import logging
import os
import re

import bugsnag
from bugsnag.flask import handle_exceptions
from flask import Flask, json
from flask_caching import Cache
from mongoengine import connect
from markdown import markdown

app = Flask(__name__)
app.debug = os.getenv('DEBUG', False)
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

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

MANIFEST_FILE = os.path.join(SITE_ROOT, "static", "manifest.json")


@cache.memoize(timeout=86400)
def manifest_path(file):
    with open(MANIFEST_FILE) as f:
        data = json.load(f)
    return data[file]


@cache.memoize(timeout=86400)
def inline_path(file):
    path = os.path.join(SITE_ROOT, manifest_path(file).lstrip('/'))
    with open(path) as f:
        content = f.read()
        return re.sub(r'^//# sourceMappingURL=.*$', '', content, flags=re.MULTILINE)


def first(list, i): return list[:i]


app.add_template_global(manifest_path, 'manifest_path')
app.add_template_global(inline_path, 'inline_path')
app.add_template_filter(markdown, 'markdown')
app.add_template_filter(first, 'first')
