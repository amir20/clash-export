FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./app /app
