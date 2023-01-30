# build stage
FROM node:16-alpine as build-stage

WORKDIR /app
COPY package*.json ./

RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY entrypoint.sh /usr/share/nginx/

RUN chmod +x "/usr/share/nginx/entrypoint.sh"
ENTRYPOINT ["/usr/share/nginx/entrypoint.sh"]

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]