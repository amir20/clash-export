import sentry_sdk
import logging
import os
from os.path import dirname, abspath

import bugsnag
import rq_dashboard
from bugsnag.flask import handle_exceptions
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_caching import Cache
from flask_graphql import GraphQLView
from flask_wtf.csrf import CSRFProtect, generate_csrf
from graphene import Schema
from mongoengine import connect
from redis import Redis


app = Flask(__name__, static_folder="_does_not_exists_", static_url_path="/static")
app.config.from_pyfile("config.py")

# Template settings
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.policies["json.dumps_kwargs"] = {"sort_keys": False}

# RQ
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

# CSRF
csrf = CSRFProtect()
csrf.init_app(app)

bugsnag.configure(
    api_key=app.config["BUGSNAG_API_KEY"],
    project_root="/app",
    release_stage=app.env,
    notify_release_stages=["production"],
    app_version=os.getenv("VERSION_TAG", "dev"),
)
handle_exceptions(app)

logging.basicConfig(level=logging.DEBUG if app.debug else logging.INFO)

# Sentry setup
sentry_sdk.init(
    dsn="https://01a0d76216d24760aeb6ae4c3a261bb2@o85378.ingest.sentry.io/6002234",
    integrations=[FlaskIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.2,
    environment=app.env,
    release=os.getenv("VERSION_TAG", "dev"),
)

# Cache settings
cache_type = "null" if app.env == "development" else "redis"
cache = Cache(app, config={"CACHE_TYPE": cache_type, "CACHE_REDIS_HOST": cache_type})

# Set connect to False for pre-forking to work
connect(db="clashstats", host="mongo", connect=False)

redis_connection = Redis("redis")

site_root = dirname(abspath(__file__))

import clashleaders.views  # noqa
import clashleaders.graphql.schema

# GraphQL
view_func = GraphQLView.as_view("graphql", schema=Schema(query=clashleaders.graphql.schema.Query))
app.add_url_rule("/graphql", view_func=view_func)


@app.before_first_request
def delete_cached_views():
    for key in redis_connection.scan_iter("flask_cache_view*"):
        redis_connection.delete(key)


@app.after_request
def inject_csrf_token(response):
    response.set_cookie("csrf_token", generate_csrf())
    return response
