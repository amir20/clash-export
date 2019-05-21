FROM node:12-alpine

# Installs latest Chromium (72) package.
RUN apk update && apk upgrade && \
  echo @edge http://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories && \
  echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories && \
  apk add --no-cache \
  chromium@edge=72.0.3626.121-r0 \
  bash \
  nss@edge \
  freetype@edge \
  harfbuzz@edge \
  ttf-freefont@edge

# Tell Puppeteer to skip installing Chrome. We'll be using the installed package.
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
ENV CHROME_EXE_PATH /usr/bin/chromium-browser

WORKDIR /app

COPY package*.json /app/
RUN npm ci

COPY . /app/

CMD [ "npm", "test"]
