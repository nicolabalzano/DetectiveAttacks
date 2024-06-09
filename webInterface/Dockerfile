FROM node:16-alpine

WORKDIR /webInterface

COPY ./package.json ./package-lock.json ./

RUN npm install

COPY . .

#RUN npm run build

RUN npm install -g serve

CMD ["npm", "run", "dev", "--", "--host"]