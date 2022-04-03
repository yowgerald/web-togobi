FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN mkdir /etc/nginx/ssl
ADD ssl/dev-web.togobi.com.pem /etc/nginx/ssl/fullchain.pem
ADD ssl/dev-web.togobi.com-key.pem /etc/nginx/ssl/privkey.pem