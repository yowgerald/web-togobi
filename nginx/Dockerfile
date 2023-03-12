FROM nginx:1.23.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN mkdir /etc/nginx/ssl
ADD ssl/_wildcard.togobi.com.pem /etc/nginx/ssl/fullchain.pem
ADD ssl/_wildcard.togobi.com-key.pem /etc/nginx/ssl/privkey.pem