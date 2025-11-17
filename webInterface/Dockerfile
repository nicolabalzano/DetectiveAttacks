FROM node:20-alpine

WORKDIR /webInterface

COPY ./package.json ./package-lock.json ./

RUN npm config set fetch-timeout 60000 && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm install --legacy-peer-deps --prefer-offline --no-audit

COPY . .

#RUN npm run build

RUN npm install -g serve

CMD ["npm", "run", "dev", "--", "--host"]