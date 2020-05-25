from typing import List

from tools import request, get_html, parse_html_for_text


async def get_list_company(name: str = None) -> List:
    """
    Получения списка компаний по имени.

    :param str name: - имя компании для поиска.
    :return List: - список словарей компаний с их данными(ИНН, название и тд)
    """
    if name is None:
        return False
    response = await request(
        name=name,
        type_='list_company',
    )
    if response:
        response = response['pageData']
        return response
    return False


async def get_list_events(guid: str = None) -> List:
    """
    Получение списка сообщений(с данными) компании по guid

    :param str guid: - уникальный идентификатор компании.
    :return List: - список словарей сообщений компании с данными.
    """
    if guid is None:
        return False
    response = await request(
        type_='list_events',
        guid=guid,
    )
    if response:
        response = response['pageData']
        return response
    return False


async def get_text_from_event(guid=None):
    """
    Получение(парсинг) блока текста из html-страницы сообщения по guid номеру

    :param str guid: - уникальный идентификатор сообщения.
    :return str: - возврат текста сообщения, в случае его нахождения, "False"
    в случае неудачи(или отстутствия текста).
    """
    if guid is None:
        return 'False'
    text = 'False'
    try:
        html = await get_html(guid)
        text = parse_html_for_text(html)
    finally:
        return text