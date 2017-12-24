# Build assets
FROM node:9-alpine as builder
WORKDIR /build
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy all files for webpack
COPY webpack.config.js .babelrc postcss.config.js ./
COPY app/assets/ app/assets/
COPY app/static/ app/static/

# Do the build
RUN npm run build


FROM python:3.6-slim

# Create app directoy
WORKDIR /app

RUN pip install pipenv

# Copy requirements file
COPY ./Pipfile* /app/

# Install packages 
RUN pipenv install --system

ARG plugins=http.expires

# Install caddy and clean up
RUN apt-get update \
    && apt-get install supervisor -y --no-install-recommends \
    && apt-get install curl -y --no-install-recommends \
    && curl --silent --show-error --fail --location \
      --header "Accept: application/tar+gzip, application/x-gzip, application/octet-stream" -o - \
      "https://caddyserver.com/download/linux/amd64?plugins=${plugins}" \
    | tar --no-same-owner -C /usr/bin/ -xz caddy \
    && chmod 0755 /usr/bin/caddy \
    && /usr/bin/caddy -version \
    && apt-get remove -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*


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
