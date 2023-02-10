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
Fixing docker issue

`export DOCKER_BUILDKIT=0`

`export COMPOSE_DOCKER_CLI_BUILD=0`

Starting the containers

`docker-compose up -d`

Create database

`docker-compose exec db_postgres bash`

`psql postgres`

`CREATE DATABASE dbtogobi;`

Run migration

`docker-compose exec web bash`

`python manage.py migrate`

`python manage.py seed-accounts`

`python manage.py seed-payments`

`python manage.py seed-togobi`

Restart Containers (optional)

`docker-compose restart`
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