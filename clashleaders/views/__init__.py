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
import clashleaders.views.similar_clans
import clashleaders.views.sitemap
import clashleaders.views.static
import clashleaders.views.status
import clashleaders.views.verified
import clashleaders.views.perf
from clashleaders import app, site_root

MANIFEST_FILE = join(site_root, "static", "manifest.json")


def manifest_path(file):
    with open(MANIFEST_FILE) as f:
        data = json.load(f)
    return data[file]


def inline_path(file):
    path = join(site_root, manifest_path(file).lstrip('/'))
    with open(path) as f:
        content = f.read()
        return re.sub(r'^//# sourceMappingURL=.*$', '', content, flags=re.MULTILINE)


def first(l, i): return l[:i]


app.add_template_global(manifest_path, 'manifest_path')
app.add_template_global(inline_path, 'inline_path')
app.add_template_filter(markdown, 'markdown')
app.add_template_filter(first, 'first')
