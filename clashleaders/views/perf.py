import time

from flask import request

from clashleaders import app


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    resp_time = (time.time() - request.start_time) * 1000
    print(resp_time)

    return response


app.before_request(start_timer)
app.after_request(stop_timer)
