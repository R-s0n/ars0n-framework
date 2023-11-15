FROM node:18.3.0-slim
RUN apt-get update
WORKDIR /app
COPY package.json /app
RUN npm install
COPY . /app
EXPOSE 3000
CMD npm start
