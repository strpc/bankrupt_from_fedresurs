import argparse

from sanic import Sanic
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse as Response
from asyncpgsa import create_pool

import handlers
import logger
import config


app = Sanic(__name__, load_env='APP_')

app.blueprint(handlers.names)
app.add_route(
    handler=handlers.index,
    uri='/',
    methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'],
    name='index',
)


@app.listener('before_server_start')
async def init_db(app: Sanic, loop):
    """
    Подключение базы данных при запуске приложения.

    :param Sanic app: - экземпляр приложения.
    :param loop: - async-луп приложения.
    """
    try:
        from time import sleep
        sleep(4)
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
    except Exception as error:
        logger.do_write_error('Error connecting database.', error)


@app.listener('after_server_stop')
async def after_server_stop(app: Sanic, loop):
    """
    Отключение базы данных после остановки сервера.

    :param Sanic app: - экземпляр приложения.
    :param loop: - async-луп приложения.
    """
    try:
        await app.pool.close()
    except Exception as error:
        logger.do_write_error('Error disconnecting database', error)


def run_app(host, port):
    """Запуск приложения"""
    app.run(
        host=host,
        port=port,
        debug=app.config.get('DEBUG', True),
        auto_reload=app.config.get('AUTORELOAD', True)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sanic app for parse information from https://fedresurs.ru/'
        )
    parser.add_argument(
        '--host', nargs='?', default='0.0.0.0', help='IP address of server'
        )
    parser.add_argument(
        '--port', '-p', nargs='?', default='8000', help='listening port'
    )
    args = parser.parse_args()

    run_app(args.host, args.port)
