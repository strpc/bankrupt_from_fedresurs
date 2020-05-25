test:
	docker exec -it app su -c "pytest -v"

postgres:
	docker stop postgres-db || true
	docker run --rm --detach --name=postgres-db \
		--env POSTGRES_USER=user \
		--env POSTGRES_PASSWORD=hackme \
		--env POSTGRES_DB=bankrupt \
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

b:
	docker exec -it $(c) su