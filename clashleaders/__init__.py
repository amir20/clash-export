import logging
import os
from os.path import dirname, abspath

import bugsnag
import rq_dashboard
from bugsnag.flask import handle_exceptions
from flask import Flask
from flask_caching import Cache
from influxdb import InfluxDBClient
from mongoengine import connect
from redis import Redis

app = Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)
app.config['REDIS_HOST'] = 'redis'
app.debug = os.getenv('DEBUG', False)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

bugsnag.configure(
    api_key=os.getenv('BUGSNAG_API_KEY'),
    project_root="/app",
    release_stage=os.getenv('STAGE', 'development'),
    notify_release_stages=["production"]
)
handle_exceptions(app)

logging.basicConfig(level=logging.INFO)

# Cache settings
cache_type = 'null' if app.debug else 'redis'
cache = Cache(app, config={'CACHE_TYPE': cache_type, 'CACHE_REDIS_HOST': 'redis'})

# Set connect to False for pre-forking to work
connect(db='clashstats', host='mongo', connect=False)

redis_connection = Redis('redis')

influx_client = InfluxDBClient(host='influx', database='clashleaders')
influx_client.create_database('clashleaders')

site_root = dirname(abspath(__file__))

import clashleaders.views  # noqa
