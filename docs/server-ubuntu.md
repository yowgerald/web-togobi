## Deployment to AWS EC2 (Ubuntu Server 22.04)

### Install necessary packages

<em>Assuming that the machine is having Python 3.10<em>

```
sudo apt-get update
```
```
sudo apt-get install supervisor \
    nginx \
    git \
    python3.10-venv \
    libpq-dev \
    python3-dev \
    build-essential
```

### Clone repo

```
cd /var/www
```
```
git clone https://github.com/yowgerald/web-togobi.git
```

### Prepare environment

Create .env file in project's root directory.

```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
```
mkdir logs/gunicorn
```

### /etc/supervisor/conf.d/gunicorn.conf

```
[program:web-togobi]
directory=/var/www/web-togobi
command=/var/www/web-togobi/venv/bin/gunicorn config.wsgi:application --workers 3 --bind 127.0.0.1:8000 --log-level info;
stdout_logfile = /var/www/web-togobi/logs/gunicorn/access.log
stderr_logfile = /var/www/web-togobi/logs/gunicorn/error.log
stdout_logfile_maxbytes=5000000
stderr_logfile_maxbytes=5000000
stdout_logfile_backups=100000
stderr_logfile_backups=100000
autostart=true
autorestart=true
startsecs=10
stopasgroup=true
priority=99
```
```
supervisorctl reread
```
```
supervisorctl update
```

### SSL

For now, this is using openssl
```
mkdir /etc/nginx/ssl && cd /etc/nginx/ssl
```
```
openssl req -x509 -nodes -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365
```

### /etc/nginx/sites-available/web-togobi

```
server {
    listen 80;
    server_name togobi.com;
    return 301 https://togobi.com$request_uri;
}
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name togobi.com;

    ssl_certificate           /etc/nginx/ssl/cert.pem;
    ssl_certificate_key       /etc/nginx/ssl/key.pem;
    ssl_protocols             TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
    location /static/ {
        alias /var/www/web-togobi/static/;
    }
}
```
### Finalize and test NGINX config
```
ln -s /etc/nginx/sites-available/web-togobi /etc/nginx/sites-enabled
```
```
nginx -t
```
```
systemctl restart nginx
```

### In EC2 and GoDaddy

1. Create elastic IP and associate it to the current EC2 instance.
2. Connect to Domain using Route53 and add records to hosted zone.
3. Change the GoDaddy's nameservers, the new values are from Route53's NS record.
