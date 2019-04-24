import json
import re
from os.path import join

from markdown import markdown

import clashleaders.views.badge
import clashleaders.views.clan
import clashleaders.views.country
import clashleaders.views.error
import clashleaders.views.export
import clashleaders.views.index
import clashleaders.views.player
import clashleaders.views.search
import clashleaders.views.sitemap
import clashleaders.views.static
import clashleaders.views.status
import clashleaders.views.troop
import clashleaders.views.verified
import clashleaders.views.explore
from clashleaders import app, site_root

MANIFEST_FILE = join(site_root, "static", "manifest.json")


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


@app.template_filter()
def first(l, i):
    return l[:i]


app.add_template_filter(markdown, "markdown")
