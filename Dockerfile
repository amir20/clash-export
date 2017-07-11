FROM python:3.6

MAINTAINER Amir Raminfar <findamir@gmail.com>

# Upgrade pip
RUN pip install --upgrade pip uwsgi

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
&& rm -rf /var/lib/apt/lists/*

# Custom Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


# Install Caddy Server, and All Middleware
RUN curl --silent --show-error --fail --location \
      --header "Accept: application/tar+gzip, application/x-gzip, application/octet-stream" -o - \
      "https://caddyserver.com/download/linux/amd64?plugins=${plugins}" \
    | tar --no-same-owner -C /usr/bin/ -xz caddy \
    && chmod 0755 /usr/bin/caddy \
    && /usr/bin/caddy -version

COPY ./caddy/Caddyfile /etc/Caddyfile

# Create app directoy
WORKDIR /app

# Install dependencies
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt


COPY ./app /app

EXPOSE 80 443
CMD ["/usr/bin/supervisord"]
