from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse as Response

import logger
from tools import (
    generate_uuid,
    uuid_from_str,
    datetime_from_string,
)
from service import get_list_company, get_list_events
from db.schema import names_table, parse_company_table, parse_event_table


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
        list_company = await get_list_company(name)
        if list_company is False:
            raise Exception('list of companies was not received')

        async with request.app.pool.acquire() as conn:  # transaction
            names_query = names_table.insert().values(
                name=name,
                local_uuid=local_uuid
            ).returning(names_table)
            names_value = await conn.fetchrow(names_query)

            for company in list_company:
                company_query = parse_company_table.insert().values(
                    link_guid=company.get('guid', generate_uuid),
                    ogrn=int(company.get('ogrn')),
                    inn=int(company.get('inn')),
                    name=str(company.get('name')),
                    address=str(company.get('address')),
                    status=str(company.get('status')),
                    status_date=datetime_from_string(
                        company.get('statusDate')
                    ),
                    primary_names_id=names_value['id']
                ).returning(parse_company_table)
                company_value = await conn.fetchrow(company_query)

                list_events = await get_list_events(company.get('guid'))
                if list_events:
                    for event in list_events:
                        # todo: получение текста
                        event_query = parse_event_table.insert().values(
                            bankrupt_name=event.get('bankruptName'),
                            data_publish=datetime_from_string(
                                event.get('datePublish')
                            ),
                            guid=event.get('guid', generate_uuid),
                            is_annuled=event.get('isAnnuled'),
                            is_locked=event.get('isLocked'),
                            is_refuted=event.get('isRefuted'),
                            number=int(event.get('number')),
                            publisher_name=event.get('publisherName'),
                            publisher_type=event.get('publisherType'),
                            title=event.get('title'),
                            type=event.get('type'),
                            text='Lorem',  # event.get(''), ###########
                            primary_parsed_company_id=company_value['id'],
                            primary_names_id=names_value['id'],
                        )
                        await conn.fetchrow(event_query)

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

# FIXME: DEV only
if __name__ == '__main__':
    from app import main
    main()
