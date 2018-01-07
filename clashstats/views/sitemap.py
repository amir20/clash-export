from flask import url_for, render_template, make_response

from clashstats import app
from clashstats.model import ClanPreCalculated


@app.route("/sitemap.xml")
def sitemap():
    pages = []
    for clan in ClanPreCalculated.objects:
        pages.append({
            'url': url_for('clan_detail_page', slug=clan.slug, _external=True),
            'modified_time': clan.last_updated.isoformat()
        })

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response
