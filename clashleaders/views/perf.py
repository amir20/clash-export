import time

from flask import request

from clashleaders import app, influx_client


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    resp_time = (time.time() - request.start_time) * 1000

    json_body = [
        {
            "measurement": "page_load",
            "tags": {
                "path": request.path,
            },
            "fields": {
                "value": resp_time
            }
        }
    ]

    influx_client.write_points(json_body)

    return response


app.before_request(start_timer)
app.after_request(stop_timer)
