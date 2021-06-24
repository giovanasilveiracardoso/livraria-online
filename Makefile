pipenv-setup:
	pipenv install

pipenv-setup-dev:
	pipenv install --dev

run-server:
	python manage.py runserver

test:
	python manage.py test --settings=livraria_online.settings.testing

coverage:
	coverage run --source='.' manage.py test --settings=livraria_online.settings.testing
	coverage report

coverage-erase:
	coverage erase

code-convention:
	flake8
	pycodestyle

collect-static:
	python manage.py collectstatic

make-migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

docker-compose-up:
	docker-compose up --build

docker-compose-down:
	docker-compose down
	docker system prune --force