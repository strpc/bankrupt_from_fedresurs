from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse as Response

import asyncio
import logger
from tools import generate_uuid, uuid_from_str
from views import parse_data, get_data_from_db


names = Blueprint(
    name='names',
    version=1
)


@names.route(uri='/names/', methods=['POST'])
async def create_task(request: Request) -> Response:
    name = None

    if request.json is not None:
        name = request.json.get('name', None)
    if name is None:
        return json(
            {'message': "key 'name' in body json is not found. please repeat "
                "the request with the key 'name'"},
            status=400
        )

    local_uuid = generate_uuid()
    try:
        pool = request.app.pool
        asyncio.gather(parse_data(local_uuid, name, pool))

        uri_check = request.app.url_for(
            'names.get_information', name=local_uuid
        )
        link_for_check = f"{request.scheme}://{request.host}{uri_check}"
        return json(
            {
                'name': name,
                'uuid': str(local_uuid),
                'link for check': link_for_check,
            },
            status=201,
            escape_forward_slashes=False
        )
    except Exception as error:
        logger.do_write_error('no database connection.', error)
        return json(
            {
                'message': 'An error has occurred. Please try again later.'
            },
            status=500
        )


@names.route(uri='/names/<name>', methods=['GET'])
async def get_information(request: Request, name: str) -> Response:
    local_uuid = uuid_from_str(name)
    pool = request.app.pool
    try:
        data = await get_data_from_db(local_uuid, pool)
        if data:
            return json(
                {
                    "data": "data",  # возвращаем данные
                },
                status=200,
            )
        else:
            raise Exception('no data found in database')
    except Exception as error:
        logger.do_write_error("Data is not found.", error)
        return json(
            {
                "message": "Data is not found. Please check 'names'",
            },
            status=404,  # нет данных
        )


@names.route(
    uri='/',
    methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']
)
async def index(request: Request) -> Response:
    logger.do_write_info('access to invalid path.', request.ip, request.url)
    return json(
        {
            "message": "path does not exist",
        },
        status=404,
    )

# FIXME: DEV only
if __name__ == '__main__':
    from app import main
    main()
