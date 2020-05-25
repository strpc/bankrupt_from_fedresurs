USER = user
PASSWORD = hackme
DB = bankrupt
PORT = 5432

test:
	docker exec -it app su -c "pytest -v"

postgres:
	docker stop postgres-db || true
	docker run --rm --detach --name=postgres-db \
		--env POSTGRES_USER=$(USER) \
		--env POSTGRES_PASSWORD=$(PASSWORD) \
		--env POSTGRES_DB=$(DB) \
		--publish 5432:5432 postgres

makemigration:
	docker exec -it app su -c "cd src/db && alembic revision --autogenerate"

migrate:
	docker exec -it app su -c "cd src/db && alembic upgrade head"

drop_table:
	docker exec -it postgres-db psql -U user -d bankrupt  -c \
	"DROP SCHEMA public CASCADE; CREATE SCHEMA public;" \
	&& docker exec -it app rm -rf ./src/db/alembic/versions/*

up:
	docker-compose up -d

upb:
	docker-compose up -d --force-recreate --build

down:
	docker-compose down

connect:
	docker exec -it $(c) su

attach:
	docker container logs -f $(c)

local_migrate:
	cd src/db && alembic upgrade head

run:
	./.venv/bin/python3 ./src/app.py

local_test:
	pytest -v

export:
	export APP_ACCESS_LOG=False && export APP_DEBUG=False && \
	export APP_PG_USER=$(USER) && export APP_PG_PASSWORD=$(PASSWORD) && \
	export APP_PG_HOST=localhost && export APP_PG_PORT=5432 && \
	export APP_PG_DATABASE=$(DB)