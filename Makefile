DC = docker-compose -f docker-compose.yml -p md2docx
DC_TESTS = docker-compose -f docker-compose.tests.yml -p md2docx-tests

API_ID = md2docx_api
API_SERVICE = api
ALEMBIC_PATH = ./backend/migrations


all: up

up:
	$(DC) up

up-build:
	$(DC) up --build

stop:
	$(DC) stop

makemigrations:
	$(DC) exec $(API_SERVICE) alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

migrate:
	$(DC) exec $(API_SERVICE) alembic upgrade head

downgrade:
	$(DC) exec $(API_SERVICE) alembic downgrade "$(filter-out $@,$(MAKECMDGOALS))"

delete-db: stop
	$(DC) rm -v api-db

recreate-db: delete-db up
	sleep 8
	$(MAKE) makemigrations "init"
	$(MAKE) migrate

clean-media:
	$(DC) exec $(API_SERVICE) sh -c "rm -rf ./api/media/*"

pandoc:
	docker exec $(API_ID) sh -c  \
		"cd ./md2docx && \
		pandoc samples/text.md \
			--reference-doc samples/reference2.docx \
			-t docx \
			--filter pandoc.py \
			-o samples/pandoc_test.docx"

tests:
	$(DC_TESTS) up --build

%:
	@: