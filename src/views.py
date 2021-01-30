from uuid import UUID
from typing import List, Union

from asyncpg.pool import Pool

from service import (
    get_list_company,
    get_list_events,
    get_text_from_event,
)
import logger
from tools import (
    generate_uuid,
    datetime_from_string,
)
from db.schema import (
    names_table,
    parse_company_table,
    parse_event_table,
)
from db.models import ListEvent


async def parse_data(local_uuid: UUID, name: str, pool: Pool):
    """
    Парсинг данных со страниц и запись их в базу данных.

    :param UUID local_uuid: - локальный(сгенерированный) uuid запроса, который
    потребутеся в дальнейшем для вызова данных из базы.
    :param str name: - запрос пользователя(имя компании для парсинга).
    :param Pool pool: - пул подключения к базе данных.
    """
    list_company = []
    try:
        list_company = await get_list_company(name)
        if list_company is False:
            raise Exception('list of companies was not received')
    except Exception as error:
        logger.do_write_error('Error getting list of companies.', error)

    try:
        async with pool.acquire() as conn:  # transaction
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
                        text = await get_text_from_event(event.get('guid'))

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
                            text=str(text),
                            primary_parsed_company_id=company_value['id'],
                            primary_names_id=names_value['id'],
                        )
                        await conn.fetchrow(event_query)

    except Exception as error:
        logger.do_write_error('An error occurred while parsing pages or '
                              'writing to the database.', error)


async def get_data_from_db(uuid: UUID, pool: Pool) -> Union[bool, List]:
    """
    Поиск локального uuid и возвращение данных из базы.

    :param UUID uuid: - локальный uuid, по которому ищутся данные в базе.
    :param Pool pool: - пул подключения к базе данных.
    :return List: - список с данными из базы данных.
    """
    if uuid is None or pool is None:
        return False
    try:
        j = parse_event_table.join(
            names_table, parse_event_table.c.primary_names_id == names_table.c.id
        )
        query_data = parse_event_table.select().with_only_columns(
            [
                parse_event_table.c.bankrupt_name,
                parse_event_table.c.title,
                parse_event_table.c.number,
                parse_event_table.c.text,
                parse_event_table.c.data_publish,
                parse_event_table.c.guid,
            ]
        ).select_from(j).where(
            names_table.c.local_uuid == uuid
        ).where(
            parse_event_table.c.type == 'BankruptcyMessage'
        )
        async with pool.acquire() as conn:
            values = ListEvent(data=await conn.fetch(query_data))
        return values

    except Exception as error:
        return False
