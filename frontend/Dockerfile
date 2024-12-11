FROM node:22.11.0

RUN mkdir -p /app/frontend

ADD package.json /package.json
ADD package-lock.json /package-lock.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
ENV VITE_API_HOST=192.168.1.12
ENV VITE_API_PORT=80
RUN npm install

WORKDIR /app/frontend
ADD . /app/frontend

RUN npm run build && npm install -g serve

ENTRYPOINT [ "/app/frontend/entrypoint.sh" ]