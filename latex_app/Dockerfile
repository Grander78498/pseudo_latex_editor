FROM amd64/node:22.11.0

RUN mkdir -p /app/frontend

ADD package.json /package.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN npm install

WORKDIR /app/frontend
ADD . /app/frontend

RUN npm run build && npm install -g serve

ENTRYPOINT [ "/app/frontend/entrypoint.sh" ]