FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

RUN pip install --upgrade pip
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./app /app
