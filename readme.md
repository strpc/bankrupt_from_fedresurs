#bankrupt_from_fedresurs
---
Тестовое задание:
```
Сайт “Федресурс” (https://fedresurs.ru) предоставляет возможность поиска информации о компании по её названию.
Например, если набрать в поиске на главной странице слово “РОМАШКА”, то будут показаны все компании, у которых в названии присутствует это слово.
При нажатии на название любой из этих компаний открывается страница с дополнительной информацией о выбранной компании - Полное наименование, сведения об имуществе, список сообщений.
Например, при открытии информации об “ООО РОМАШКА” (https://fedresurs.ru/company/971b80ca-06fe-4bfd-98eb-07d5aeda004b) можно увидеть, что у них есть 29 сообщений.
Требуется:
1. Реализовать метод сбора всех сообщений по заданной ключевой фразе и оставить среди всех сообщений только упоминания о банкротстве. Из сообщений нужно извлечь уникальный идентификатор, текст, дату публикации и url
2. Реализовать HTTP сервис, со следующими endpoint’ами:
a. получить задание - на вход ключевик для поиска, возвращает guid задания,
b. показать результат - на вход guid задания, возвращает json со всеми
сообщениями, полученными методом из п. 1 3. Реализовать сервис как docker контейнер
Опционально:
1. Реализовать хранение промежуточных данных в любой привычной БД
2. Реализовать логгирование получения и выполнения заданий любым привычным
способом
```
---
API:

**Создать задание:**<br>
`curl --request POST --url http://localhost:8000/v1/names/ --header 'content-type: application/json' --data '{"name": "Иванов"}'`
<br>Ответ:
```
< HTTP/1.1 202 Accepted
< Content-Length: 180
< Content-Type: application/json
< Connection: keep-alive
< Keep-Alive: 5
body:
{
  "name": "Иванов",
  "uuid": "b5d1ac5c-95f6-49e6-ae9c-984a6abf5e61",
  "link for check": "http://localhost:8000/v1/names/b5d1ac5c-95f6-49e6-ae9c-984a6abf5e61"
}
```

**Проверить задание:**<br>
`curl --request GET --url http://localhost:8000/v1/names/b5d1ac5c-95f6-49e6-ae9c-984a6abf5e61 --header 'content-type: application/json'`
<br>Ответ:
```
< HTTP/1.1 200 OK
< Content-Length: 2383
< Content-Type: application/json
< Connection: keep-alive
< Keep-Alive: 5
body:
{
  "uuid": "51da50de-ae1e-4ecb-a7b7-f92143b513ea",
  "messages": [
    ..data..
  ]
}
```
Приложение также хранит промежуточные данные в PostgreSQL, которые в дальнейшем можно будет использовать.

---
Запуск в Docker:<br>
```
git clone https://github.com/strpc/bankrupt_from_fedresurs.git
cd bankrupt_from_fedresurs
docker-compose up -d
docker exec -it app su -c "cd src/db && alembic upgrade head"
```

Запуск локально(Pythom>=3.6, также необходимо установить переменные окружения: APP_ACCESS_LOG=False, APP_DEBUG=False, APP_PG_USER=user, APP_PG_PASSWORD=hackme, APP_PG_HOST=db, APP_PG_PORT=5432, APP_PG_DATABASE=bankrupt):<br>
```
git clone https://github.com/strpc/bankrupt_from_fedresurs.git
cd bankrupt_from_fedresurs
pip install -r requirements.txt
docker run --rm --detach --name=postgres-db \
		--env POSTGRES_USER=user \
		--env POSTGRES_PASSWORD=hackme \
		--env POSTGRES_DB=bankrupt \
		--publish 5432:5432 postgres
cd src/db && alembic upgrade head
python3 app.py
```

Запуск тестов: <br>
```
docker exec -it app su -c "pytest -v" (docker)
или
pytest -v (локально)
```