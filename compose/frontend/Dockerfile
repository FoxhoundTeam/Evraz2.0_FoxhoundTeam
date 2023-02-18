# develop stage
FROM node:18.13.0-alpine as develop-stage
WORKDIR /app
RUN npm install -g yarn@latest --force && \
    yarn global add @vue/cli

# build stage
FROM develop-stage as build-stage
RUN apk add git
COPY ./frontend/package.json ./frontend/yarn.lock ./
RUN yarn install --frozen-lockfile
COPY ./frontend .
RUN yarn build

# production stage
FROM nginx:1.17.5-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]