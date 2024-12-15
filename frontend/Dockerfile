FROM node:22.11.0

RUN mkdir -p /app/frontend

ADD package.json /package.json
ADD package-lock.json /package-lock.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
ENV VITE_API_HOST=localhost
ENV VITE_API_PORT=80
RUN npm install

WORKDIR /app/frontend
ADD . /app/frontend
RUN chmod +x /app/frontend/entrypoint.sh

RUN npm run build

ENTRYPOINT [ "/app/frontend/entrypoint.sh" ]