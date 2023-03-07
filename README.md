# Documentation

### Create certificate
`mkcert -install`

`cd nginx/ssl`

`mkcert "*.togobi.com"`
<br/>

### Credentials & Keys (.credentials/)
* service_account.json
<br/>

### Local Setup with Docker
Starting the containers

`docker-compose up -d`

Run migration

`docker-compose exec web bash`

`python manage.py migrate`

`python manage.py seed-accounts`

`python manage.py seed-payments`

`python manage.py seed-togobi`
<br/>

## Common Django Commands

migrate - `python manage.py migrate`

run - `python manage.py runserver`

create admin user - `winpty python manage.py createsuperuser`

create an app - `python manage.py startapp 'accounts'`

create app migrations - `python manage.py makemigrations 'accounts'`

migrate app - `python manage.py migrate 'accounts'`

clean db - `python manage.py flush`

shell - `python manage.py shell`


## NOTES:
* Service account should have storage admin access
* When connecting to postgres outside docker, use the port `6543`
* DBeaver for database management