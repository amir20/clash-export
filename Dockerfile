FROM python:3.6

MAINTAINER Amir Raminfar <findamir@gmail.com>

# Upgrade pip
RUN pip install --upgrade pip uwsgi

# Create app directoy
WORKDIR /app

# Install dependencies
COPY ./conf/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Caddy Server, and All Middleware
RUN curl --silent --show-error --fail --location \
      --header "Accept: application/tar+gzip, application/x-gzip, application/octet-stream" -o - \
      "https://caddyserver.com/download/linux/amd64?plugins=${plugins}" \
    | tar --no-same-owner -C /usr/bin/ -xz caddy \
    && chmod 0755 /usr/bin/caddy \
    && /usr/bin/caddy -version


# Custom Supervisord config
COPY ./conf/supervisord-web.conf /etc/supervisor/conf.d/supervisord.conf

# Copy caddy file
COPY ./caddy/Caddyfile /etc/Caddyfile

# Copy all other files
COPY ./app /app

EXPOSE 80 443
CMD ["/usr/bin/supervisord"]
