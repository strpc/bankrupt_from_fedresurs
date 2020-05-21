from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse as Response

from tools import generate_uuid, uuid_from_str
import logger


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
        # TODO: запрос в базу с созданием записи c local_uuid
        # TODO: выполнение парсинга страниц
        uri_check = request.app.url_for('names.get_information', name=local_uuid)
        return json(
            {
                'name': name,
                'uuid': str(local_uuid),
                'link for check': f"{request.scheme}://{request.host}{uri_check}",
            },
            status=201,
            escape_forward_slashes=False
        )
    except Exception as error:
        logger.do_write_error('Error writing to database.', error)
        return json(
            {
                'message': 'An error has occurred. Please try again later.'
            },
            status=500
        )


@names.route(uri='/names/<name>', methods=['GET'])
async def get_information(request: Request, name: str) -> Response:
    local_uuid = uuid_from_str(name)
    try:
        # TODO: запрос в БД, поиск по uuid
        # TODO: возврат значений.
        # todo: возврат json со значениями
        count = "select"

        if count:
            return json(
                {
                    "data": "data",  # возвращаем данные
                },
                status=200,
            )

        return json(
            {
                "message": "Data is not found. Please check 'names'",
            },
            status=404,  # нет данных
        )

    except Exception as error:
        # fixme: заполнить ошибку
        logger.do_write_error("Eror reading from database.", error)
        return json(
            {
                'message': 'An error has occurred. Please try again later.',
            },
            status=500,
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