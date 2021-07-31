# Documentation

## Common Django Commands

migrate - `python manage.py migrate`

run - `python manage.py runserver`

create admin user - `winpty python manage.py createsuperuser`

create an app - `python manage.py startapp <accounts>`

create app migrations - `python manage.py makemigrations <accounts>`

migrate app - `python manage.py migrate <accounts>`

clean db - `python manage.py flush`

shell - `python manage.py shell`

<br/>

## Deployment to Linode (Centos 8):

### Install nginx
`yum install nginx`

`systemctl start nginx`

`systemctl enable nginx`

`systemctl stop firewalld` -> https://linuxize.com/post/how-to-stop-and-disable-firewalld-on-centos-7/


### Install python 3.8
`yum install gcc openssl-devel bzip2-devel libffi-devel`

`yum install wget`

`wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz`

`yum install tar`

`tar xzf Python-3.8.0.tgz`

`cd Python-3.8.0`

`./configure --enable-optimizations`

`yum install make`

`make altinstall`


### Install pip
`wget https://bootstrap.pypa.io/get-pip.py`

`pip install --upgrade pip`

### Get, setup project
`yum install git`

`git clone 'project'`

`cd 'project'`

add config files like .env
`chmod 600 client-key.pem`

`python3.8 -m venv venv`

`source venv/bin/activate`


### Preparation for postgresql
`yum groupinstall "Development Tools"`

`yum install python3-devel`

`yum install postgresql-libs`

`yum install postgresql-devel`

`wget -qO- https://ipecho.net/plain ; echo` -> add public ip to gcloud psql authorization


### Install project packages
`pip install -r requirements.txt`

`pip install django-settings-export` -> need to be separated as of now

`python manage.py collectstatic`

### Install libmediainfo for checking file
`yum --enablerepo extras install epel-release`

`cd ..`

`wget http://mirror.centos.org/centos/8/PowerTools/x86_64/os/Packages/tinyxml2-6.0.0-3.el8.x86_64.rpm`

`yum localinstall tinyxml2-6.0.0-3.el8.x86_64.rpm`

`yum install libmediainfo`

### Test run
`cd 'project'`

`python manage.py runserver 0.0.0.0:8000`

`gunicorn --bind 0.0.0.0:8000 config.wsgi:application`

### Background run
`sestatus`

`nano /etc/selinux/config`

// Replace with 

`SELINUX=permissive`

`systemctl stop firewalld` -> may need to run again after boot up

### /etc/systemd/system/gunicorn.service
```
[Unit]
Description=gunicorn daemon
After=network.target
[Service]
User=root
Group=nginx
WorkingDirectory=/var/'project'
ExecStart=/var/'project'/venv/bin/gunicorn --workers 3 --log-level debug --error-logfile /var/'project'/error.log --bind unix:/var/'project'/app.sock config.wsgi:application
[Install]
WantedBy=multi-user.target
```

systemctl restart gunicorn
systemctl enable gunicorn
systemctl status gunicorn

### /etc/nginx/nginx.conf
```
server {
    listen 80;
    server_name 'IP';
location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/project;
    }
location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/var/project/app.sock;
    }
}
```

`systemctl restart nginx`

### Optional for permissions
`usermod -a -G centos nginx`
`chmod 710 /var/'project'`

<br/>