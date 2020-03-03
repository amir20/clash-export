import logging
import os
from os.path import dirname, abspath

import bugsnag
import rq_dashboard
from bugsnag.flask import handle_exceptions
from flask import Flask
from flask_caching import Cache
from flask_graphql import GraphQLView
from graphene import Schema
from mongoengine import connect
from redis import Redis

app = Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)
app.config["REDIS_HOST"] = "redis"
app.debug = os.getenv("DEBUG", False)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

bugsnag.configure(
    api_key=os.getenv("BUGSNAG_API_KEY"), project_root="/app", release_stage=os.getenv("STAGE", "development"), notify_release_stages=["production"]
)
handle_exceptions(app)

logging.basicConfig(level=logging.INFO)

# Cache settings
cache_type = "null" if app.debug and not os.getenv("ENABLE_CACHE", False) else "redis"
cache = Cache(app, config={"CACHE_TYPE": cache_type, "CACHE_REDIS_HOST": "redis"})

# Set connect to False for pre-forking to work
connect(db="clashstats", host="mongo", connect=False)

redis_connection = Redis("redis")

site_root = dirname(abspath(__file__))

import clashleaders.views  # noqa
import clashleaders.graphql.schema

view_func = GraphQLView.as_view("graphql", schema=Schema(query=clashleaders.graphql.schema.Query), graphiql=True)
app.add_url_rule("/graphql", view_func=view_func)


@app.before_first_request
def delete_cached_views():
    for key in redis_connection.scan_iter("flask_cache_view*"):
        redis_connection.delete(key)
