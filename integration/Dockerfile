FROM amir20/docker-alpine-puppeteer:v1

COPY package*.json /app/
RUN npm ci

COPY . /app/

CMD ["npm", "test"]
