from flask import url_for, render_template, make_response

from clashleaders import app
from clashleaders.model import ClanPreCalculated


@app.route("/sitemap.xml")
def sitemap():
    pages = []

    pages.append({'url': url_for('index', _external=True)})

    for clan in ClanPreCalculated.objects.only('slug'):
        pages.append({
            'url': url_for('clan_detail_page', slug=clan.slug, _external=True),
        })

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response
