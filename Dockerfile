# Build assets
FROM node:9-alpine as builder

RUN apk add --no-cache git openssh

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


FROM python:3.6-slim

# Create app directoy
WORKDIR /app

RUN pip install pipenv

# Copy requirements file
COPY ./Pipfile* /app/

ARG plugins=http.expires

# Install caddy and clean up
RUN apt-get update \
    && apt-get install supervisor -y --no-install-recommends \
    && apt-get install curl -y --no-install-recommends \
    && apt-get install gcc -y \
    && curl --silent --show-error --fail --location \
      --header "Accept: application/tar+gzip, application/x-gzip, application/octet-stream" -o - \
      "https://caddyserver.com/download/linux/amd64?plugins=${plugins}" \
    | tar --no-same-owner -C /usr/bin/ -xz caddy \
    && chmod 0755 /usr/bin/caddy \
    && /usr/bin/caddy -version \
    && pipenv install --system \
    && apt-get remove -y curl gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

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
