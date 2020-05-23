run:
	./.venv/bin/python3 ./src/app.py

test:
	./.venv/bin/pytest -v

postgres:
	docker stop bankrupt-bd || true
	docker run --rm --detach --name=bankrupt-bd \
		--env POSTGRES_USER=user \
		--env POSTGRES_PASSWORD=hackme \
		--env POSTGRES_DB=bankrupt \
		--publish 5432:5432 postgres

makemigration:
	cd src/db && alembic revision --autogenerate

migrate:
	cd src/db && alembic upgrade head

drop_table:
	docker exec -it bankrupt-bd psql -U user -d bankrupt  -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" && rm -rf ./src/db/alembic/versions/*