FROM amir20/docker-alpine-puppeteer:v2

COPY package*.json /app/
RUN npm ci

COPY . /app/

CMD ["npm", "test"]
