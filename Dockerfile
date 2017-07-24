# Build assets
FROM node:8-alpine as builder
WORKDIR /build
COPY package*.json ./

# Install dependencies
RUN npm i

# Copy all files for webpack
COPY webpack.config.js .babelrc postcss.config.js ./
COPY app/javascript/ app/javascript/
COPY app/static/ app/static/

# Do the build
RUN npm run build


FROM python:3.6-alpine

MAINTAINER Amir Raminfar <findamir@gmail.com>

# Install supervisord
RUN apk add --no-cache supervisor

# Create app directoy
WORKDIR /app

# Copy requirements file
COPY ./conf/requirements.txt /app/requirements.txt

ARG plugins

# Install packages and docker
RUN apk add --no-cache --virtual .apk-deps \
    curl \
    gcc \
    libc-dev \
    linux-headers \
    && pip install -r /app/requirements.txt \
    && curl --silent --show-error --fail --location \
      --header "Accept: application/tar+gzip, application/x-gzip, application/octet-stream" -o - \
      "https://caddyserver.com/download/linux/amd64?plugins=${plugins}" \
    | tar --no-same-owner -C /usr/bin/ -xz caddy \
    && chmod 0755 /usr/bin/caddy \
    && /usr/bin/caddy -version \
    && apk del .apk-deps


# Custom Supervisord config
COPY ./conf/supervisord-web.conf /etc/supervisor/conf.d/supervisord.conf

# Copy caddy file
COPY ./caddy/Caddyfile /etc/Caddyfile

# Copy all other files
COPY ./app /app

# Copy the js files
COPY --from=builder /build/app/static /app/static


VOLUME /root/.caddy
EXPOSE 80 443
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
