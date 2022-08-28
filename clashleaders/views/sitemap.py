from math import ceil

from flask import make_response, render_template, url_for

from clashleaders import app, cache
from clashleaders.model import Clan

TOTAL_PER_PAGE = 10000


@app.route("/sitemap_index.xml")
def sitemap_index():
    sitemaps = []

    pages = ceil(Clan.estimated_count() / TOTAL_PER_PAGE)
    for i in range(pages):
        sitemaps.append({"url": url_for("sitemap", page=i, _external=True)})

    sitemap_xml = render_template("sitemap_index.xml", sitemaps=sitemaps)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route("/sitemap_<page>.xml")
@cache.cached(36000)
def sitemap(page):
    start = int(page) * TOTAL_PER_PAGE
    end = start + TOTAL_PER_PAGE

    pages = ({"url": url_for("clan_detail_page", slug=clan.slug, _external=True)} for clan in Clan.objects[start:end].no_cache().only("slug"))

    sitemap_xml = render_template("sitemap.xml", pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response
