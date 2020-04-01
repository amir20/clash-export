FROM alpine:edge


RUN echo @edge http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories && \
  apk add --no-cache \
  chromium \
  nss \
  freetype \
  freetype-dev \
  harfbuzz \
  ca-certificates \
  ttf-freefont \
  nodejs \
  npm \
  python \
  g++ \
  make \
  bash \
  font-noto-emoji@edge \
  wqy-zenhei@edge

# Tell Puppeteer to skip installing Chrome. We'll be using the installed package.
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
ENV CHROME_EXE_PATH /usr/bin/chromium-browser

RUN addgroup -S pptruser && adduser -S -g pptruser pptruser \
  && mkdir -p /home/pptruser/Downloads /app \
  && chown -R pptruser:pptruser /home/pptruser \
  && chown -R pptruser:pptruser /app

USER pptruser

WORKDIR /app

COPY --chown=pptruser:pptruser package*.json /app/
RUN npm ci

COPY --chown=pptruser:pptruser . /app/

CMD [ "npm", "test"]
