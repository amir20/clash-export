import base64
import hashlib
import hmac
import json
from math import ceil
import os
import re
import textwrap
from os.path import join

from markdown import markdown

import clashleaders.views.badge
import clashleaders.views.clan
import clashleaders.views.tag
import clashleaders.views.country
import clashleaders.views.error
import clashleaders.views.explore
import clashleaders.views.index
import clashleaders.views.player
import clashleaders.views.sitemap
import clashleaders.views.static
import clashleaders.views.status
import clashleaders.views.troop
import clashleaders.views.verified
import clashleaders.views.multi_export
from clashleaders import app, site_root

MANIFEST_FILE = join(site_root, "static", "manifest.json")
IMGPROXY_KEY = bytes.fromhex(os.getenv("IMGPROXY_KEY", "01"))
IMGPROXY_SALT = bytes.fromhex(os.getenv("IMGPROXY_SALT", "01"))
IMGPROXY_BASE = os.getenv("IMGPROXY_BASE", "https://i.clashleaders.com/")

GRADES = [
    "Max",
    "A+",
    "A",
    "A-",
    "B+",
    "B",
    "B-",
    "C+",
    "C",
    "C-",
    "D+",
    "D",
    "D-",
    "E",
    "E",
    "E",
    "F",
]
CLASSES = {
    "M": "has-text-success",
    "A": "has-text-success",
    "B": "has-text-grey",
    "C": "has-text-grey",
    "D": "has-text-danger",
    "E": "has-text-danger",
    "F": "has-text-danger",
}


# This is needed for mocking
def manifest_map():
    with open(MANIFEST_FILE) as f:
        return json.load(f)


@app.template_global()
def manifest_path(file):
    return manifest_map()[file]


@app.template_global()
def inline_path(file):
    path = join(site_root, manifest_path(file).lstrip("/"))
    with open(path) as f:
        content = f.read()
        return re.sub(r"^//# sourceMappingURL=.*$", "", content, flags=re.MULTILINE)


@app.template_global()
def imgproxy_url(url):
    encoded_url = base64.urlsafe_b64encode(url.encode()).rstrip(b"=").decode()
    encoded_url = "/".join(textwrap.wrap(encoded_url, 16))
    path = "/{encoded_url}".format(encoded_url=encoded_url).encode()
    digest = hmac.new(
        IMGPROXY_KEY, msg=IMGPROXY_SALT + path, digestmod=hashlib.sha256
    ).digest()
    protection = base64.urlsafe_b64encode(digest).rstrip(b"=")
    return (b"%s%s%s" % (IMGPROXY_BASE.encode(), protection, path)).decode()


@app.template_global()
def scorecard_class(grade):
    first = grade[0]
    return CLASSES.get(first, "")


@app.template_global()
def scorecard(value):
    s = ceil((100 - value * 100) / 3)
    return GRADES[min(s, len(GRADES) - 1)]


@app.template_filter()
def first(l, i):
    return l[:i]


app.add_template_filter(markdown, "markdown")
