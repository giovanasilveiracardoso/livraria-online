## Requirements

- Python 3.9.5
- Pip
- PostgreSQL

or

- Docker (https://docs.docker.com/engine/install/ubuntu/)
- Docker compose (https://docs.docker.com/compose/install/)

Optional:

- Pipenv
- Make

You can install all dependencies and creating a virtualenv with pipenv (https://pipenv.readthedocs.io/en/latest/install/)
by running:

`pipenv install`

or

`make pipenv-setup`

In PostgreSQL, create a database named "livraria" and apply all migrations:

`python manage.py migrate`

## API docs

`/docs`

## Running 

### Local

`python manage.py runserver`<br>
or<br>
`make run-server`

### Docker compose

`docker-compose up --build`

## Tests

For tests running, you should install all development dependencies. It can be installed with pipenv by running:

`pipenv install --dev`

or

`make pipenv-setup-dev`

Run all project tests with:

`python manage.py test --settings=livraria_online.settings.testing`

or

`make test`

### Coding style tests

This project uses flake8 and pycodestyle checking. Install all development dependencies and execute:

`flake8 & pycodestyle`

or

`make code-convention`

## Coverage

For coverage running, you should install all development dependencies. See [Tests section](#Tests).

Run project coverage with:

`coverage run --source='.' manage.py test --settings=livraria_online.settings.testing`

or

`make coverage`

## Django Admin

Create superuser:

`sudo docker exec -it id_container /bin/bash`

`python manage.py createsuperuser`

## Author

**Giovana Cardoso Berti** - (https://github.com/giovanasilveiracardoso)



