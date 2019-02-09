import time

from flask import request
from influxdb import InfluxDBClient

from clashleaders import app

client = InfluxDBClient(host='influx', database='clashleaders')
client.create_database('clashleaders')


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    resp_time = (time.time() - request.start_time) * 1000

    json_body = [
        {
            "measurement": "page_load_times",
            "tags": {
                "path": request.full_path,
            },
            "fields": {
                "value": resp_time
            }
        }
    ]

    client.write_points(json_body)

    return response


app.before_request(start_timer)
app.after_request(stop_timer)
