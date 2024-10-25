# Build assets
FROM node:20.18.0 as builder

RUN corepack enable

WORKDIR /build
COPY pnpm-lock.yaml ./
RUN pnpm fetch

# Install build dependencies
COPY package.json ./
RUN pnpm install -r --offline

# For building js version
ARG VERSION_TAG=DIRTY
ENV VERSION_TAG $VERSION_TAG

# Copy all files for webpack
COPY webpack* .* ./
COPY assets/ assets/
COPY clashleaders/static clashleaders/static

# Do the build
RUN pnpm build


FROM python:3.12.2

# Create app directoy
WORKDIR /app

# Copy requirements file
COPY ./requirements.txt ./pyproject.toml /app/


# Add caddy sources
RUN echo "deb [trusted=yes] https://apt.fury.io/caddy/ /" \
  | tee -a /etc/apt/sources.list.d/caddy-fury.list

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH /root/.cargo/bin:$PATH
ENV UV_SYSTEM_PYTHON true

# Install caddy and clean up
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install cron curl caddy make supervisor -y --no-install-recommends \
  && apt-get install python3-cairo python3-cairosvg libfreetype6-dev libxft-dev -y \
  && uv pip install -r requirements.txt \
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
COPY ./Makefile ./MANIFEST.in /app/
COPY ./*.json /app/
COPY ./*.py /app/

RUN uv pip install -e .

# Copy the js files
COPY --from=builder /build/clashleaders/static /app/clashleaders/static


ENV FLASK_APP=clashleaders
ARG SOURCE_COMMIT=DIRTY
ENV SOURCE_COMMIT $SOURCE_COMMIT
ARG VERSION_TAG=DIRTY
ENV VERSION_TAG $VERSION_TAG

VOLUME /root/.caddy

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord-web.conf"]
