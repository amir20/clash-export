# Build assets
FROM node:9-alpine as builder

RUN apk add --no-cache git openssh python make g++

WORKDIR /build
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy all files for webpack
COPY webpack.config.js .babelrc postcss.config.js ./
COPY assets/ assets/
COPY clashleaders/static clashleaders/static

# Do the build
RUN npm run build


FROM python:3.6.5-slim

# Create app directoy
WORKDIR /app

RUN pip install pipenv

# Copy requirements file
COPY ./Pipfile* /app/

ARG plugins=http.expires

# Install caddy and clean up
RUN apt-get update \
    && apt-get install make supervisor -y --no-install-recommends \
    && apt-get install curl -y --no-install-recommends \
    && apt-get install gcc -y \
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
COPY ./*.py /app/

# Copy the js files
COPY --from=builder /build/clashleaders/static /app/clashleaders/static

RUN pip install -e .
ENV FLASK_APP=clashleaders

VOLUME /root/.caddy
EXPOSE 80 443
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord-web.conf"]
