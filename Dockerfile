# Build assets
FROM node:13-alpine as builder

RUN apk add --no-cache git openssh python make g++ \
    && npm install -g npm

WORKDIR /build
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy all files for webpack
COPY webpack* .babelrc ./
COPY assets/ assets/
COPY clashleaders/static clashleaders/static

# Do the build
RUN npm run build


FROM python:3.8.2

# Create app directoy
WORKDIR /app

# Copy requirements file
COPY ./requirements*.txt /app/

ARG plugins=http.expires

# Install caddy and clean up
RUN apt-get update \
    && pip install --upgrade pip \
    && apt-get install make supervisor -y --no-install-recommends \
    && apt-get install curl -y --no-install-recommends \
    && apt-get install cron -y \
    && apt-get install python3-cairo python3-cairosvg libfreetype6-dev libxft-dev -y \
    && curl https://getcaddy.com | bash -s personal ${plugins} \
    && pip install --no-cache -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache

# Install cron jobs
COPY ./conf/crontab /etc/cron.d/clashleaders
COPY ./conf/cron.sh /usr/local/bin/cron.sh
RUN chmod 0644 /etc/cron.d/clashleaders
RUN crontab /etc/cron.d/clashleaders
RUN chmod +x /usr/local/bin/cron.sh


COPY ./conf/supervisord-*.conf /etc/supervisor/conf.d/
COPY ./caddy/Caddyfile /etc/Caddyfile
COPY ./caddy /etc/caddy
COPY ./conf/gunicorn.conf.py /app/

COPY ./clashleaders /app/clashleaders
COPY ./tests /app/tests
COPY ./Makefile /app/
COPY ./setup.cfg /app/
COPY ./*.json /app/
COPY ./*.py /app/


# Copy the js files
COPY --from=builder /build/clashleaders/static /app/clashleaders/static

RUN pip install -e .
ENV FLASK_APP=clashleaders
ARG SOURCE_COMMIT=DIRTY
ENV SOURCE_COMMIT $SOURCE_COMMIT

VOLUME /root/.caddy

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord-web.conf"]
