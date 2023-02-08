# Documentation

### Create certificate
`mkcert -install`

`cd nginx/ssl`

`mkcert "*.togobi.com"`

### Local Setup with Docker
`export DOCKER_BUILDKIT=0`

`export COMPOSE_DOCKER_CLI_BUILD=0`

`docker-compose up -d`

`docker-compose exec web bash`

`python manage.py migrate`

## Common Django Commands

migrate - `python manage.py migrate`

run - `python manage.py runserver`

create admin user - `winpty python manage.py createsuperuser`

create an app - `python manage.py startapp 'accounts'`

create app migrations - `python manage.py makemigrations 'accounts'`

migrate app - `python manage.py migrate 'accounts'`

clean db - `python manage.py flush`

shell - `python manage.py shell`

<br/>
