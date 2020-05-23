from sanic import Sanic
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse as Response
from asyncpgsa import create_pool

import views
import logger
import config


app = Sanic(__name__)
app.config.from_object(config)

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
        host=app.config.PG_HOST,
        port=app.config.PG_PORT,
        user=app.config.PG_USER,
        password=app.config.PG_PASSWORD,
        database=app.config.PG_DATABASE,
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
        auto_reload=False,
        RESPONSE_TIMEOUT=20
    )


if __name__ == '__main__':
    main()
