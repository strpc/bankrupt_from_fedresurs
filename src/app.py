from sanic import Sanic
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse as Response
from asyncpgsa import create_pool

import views
import logger
from config import (
    PG_USER,
    PG_PASSWORD,
    PG_HOST,
    PG_PORT,
    PG_DATABASE,
)


app = Sanic(__name__)

app.blueprint(views.names)
app.add_route(
    handler=views.index,
    uri='/',
    methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'],
    name='index',
)


@app.listener('before_server_start')
async def register_db(app, loop):
    app.pool = await create_pool(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        database=PG_DATABASE,
        loop=loop,
        min_size=5,
        max_size=100
    )


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    try:
        await app.pool.close()
    except Exception as error:
        logger.do_write_error('Error disconnecting database', error)


def main():
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        # auto_reload=False,
    )


if __name__ == '__main__':
    main()
