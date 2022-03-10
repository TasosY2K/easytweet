FROM node:16-alpine

WORKDIR /easytweet_frontend

COPY ./ ./

RUN npm install
RUN npm run lintfix
RUN npm run build
RUN npm run generate

EXPOSE 3000

ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

CMD ["npm", "run", "start"]