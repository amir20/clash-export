# Build assets
FROM node:10-alpine as builder

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


FROM python:3.6.5-slim

# Create app directoy
WORKDIR /app

RUN pip install --upgrade pip \ 
    && pip install pipenv

# Copy requirements file
COPY ./Pipfile* /app/

ARG plugins=http.expires

# Install caddy and clean up
RUN apt-get update \
    && apt-get install make supervisor -y --no-install-recommends \
    && apt-get install curl -y --no-install-recommends \
    && apt-get install gcc -y \
    && apt-get install python3-cairo python3-cairosvg libfreetype6-dev libxft-dev -y \
    && curl https://getcaddy.com | bash -s personal ${plugins} \
    && pipenv install --system \
    && apt-get remove -y curl gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache

# Custom Supervisord config
COPY ./conf/supervisord-*.conf /etc/supervisor/conf.d/

# Copy caddy file
COPY ./caddy/Caddyfile /etc/Caddyfile

# Copy all other files
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
EXPOSE 80 443
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord-web.conf"]
