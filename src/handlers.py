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
    """
    Обработчик POST-запроса для создания задачи по сбору информации о компаниях.
    Ожидается json формата:
    {
        "name": "Иванов"
    }
    где "Иванов" - название компании.

    Ответ:
    < HTTP/1.1 202 Accepted
    < Content-Length: 180
    < Content-Type: application/json
    < Connection: keep-alive
    < Keep-Alive: 5

    body:
    {
    "name": "Иванов",
    "uuid": "d32e302c-7d86-4f1d-9295-370bbcf20c63",
    "link for check": "http://localhost:8000/v1/names/d32e302c-7d86-4f1d-9295-370bbcf20c63"
    }

    :param Request request: - тело запроса.
    """
    name = None
    if request.json is not None:
        name = request.json.get('name', None)
    if name is None:
        return json({
            'message': "key 'name' in body json is not found. please repeat "
            "the request with the key 'name'"
        },
            status=400,
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
            status=202,
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
    """
    Обработчик GET-запроса на получение собранной информации.
    URI формата /names/UUID

    Ответ:
    < HTTP/1.1 200 OK
    < Content-Length: 255074
    < Content-Type: application/json
    < Connection: keep-alive
    < Keep-Alive: 5

    body:
    {
    "uuid": "1ecd65a6-8c50-4291-b3a3-803c0e82c16e",
    "messages": [ data]
    }

    :param Request request: - тело запроса.
    :param str name: - сгенерированный при POST-запросе уникальный иднетификатор
    """
    try:
        pool = request.app.pool
    except Exception as error:
        logger.do_write_error('no database connection', error)

    try:
        local_uuid = uuid_from_str(name)
    except Exception as error:
        logger.do_write_error('invalid uuid entered', error)
        return json(
            {
                "message": "Invalid uuid",
            },
            status=400,  # нет данных
        )

    try:
        data = await get_data_from_db(local_uuid, pool)
        if data:
            return json(
                {
                    "uuid": name,
                    "messages": list(data.dict().values())[0],
                },
                status=200,
                escape_forward_slashes=False,
                encode_html_chars=True,
                ensure_ascii=False,
            )
        else:
            raise Exception('Data is not found.')

    except Exception as error:
        logger.do_write_error(error)
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
    """
    Обработчик несуществующих URI.

    :param Request request: - тело запроса.
    """
    logger.do_write_info('access to invalid path.', request.ip, request.url)
    return json(
        {
            "message": "path does not exist",
        },
        status=404,
    )
