from bs4 import BeautifulSoup
import httpx

import datetime
import logger
from os.path import join as path_join, abspath
import uuid
from typing import Union, Text


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def uuid_from_str(data: str = None) -> uuid.UUID:
    if data is None:
        return False
    return uuid.UUID(data)


async def request(
    name: str = None,
    type_: Union['list_company', 'list_events', ] = None,
    guid: str = None
) -> httpx.Response.json:
    """
    HTTP-запросы к сервису.

    :param str name: имя компании для поиска.
    :param str type_: тип запроса(запрос списка компаний или списка сообщений).
    :return dict:
    """
    if type_ not in ('list_company', 'list_events',):
        return False
    cookies = {}

    if type_ == 'list_company' and isinstance(name, str):
        url = 'https://fedresurs.ru/backend/companies/search'
        data = {
            "entitySearchFilter": {
                "onlyActive": True,
                "startRowIndex": 0,
                "pageSize": 100000,
                "name": name,
            },
        }
        make_referer = str(httpx.URL(
            'https://fedresurs.ru/search/entity',
            params={'name': name}
        ))
        headers = {
            'accept': "application/json, text/plain, */*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            'content-type': "application/json",
            'origin': "https://fedresurs.ru",
            'referer': make_referer,
        }

    elif type_ == 'list_events' and guid is not None:
        url = 'https://fedresurs.ru/backend/companies/publications'
        data = {
            "guid": guid,
            "pageSize": 100000,
            "startRowIndex": 0,
            "startDate": None,
            "endDate": None,
            "messageNumber": None,
            "bankruptMessageType": None,
            "bankruptMessageTypeGroupId": None,
            "legalCaseId": None,
            "searchAmReport": True,
            "searchFirmBankruptMessage": True,
            "searchFirmBankruptMessageWithoutLegalCase": False,
            "searchSfactsMessage": False,
            "searchSroAmMessage": False,
            "searchTradeOrgMessage": False,
            "sfactMessageType": None,
            "sfactsMessageTypeGroupId": None
        }
        headers = {
            'accept': "application/json, text/plain, */*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            'referer': "https://fedresurs.ru/company/971b80ca-06fe-4bfd-98eb-07d5aeda004b",
            'content-type': "application/json"
        }
    else:
        return False

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        return response.json()


async def get_html(guid: str = None) -> Text:
    if guid is None:
        return False
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/81.0.4044.138 Safari/537.36',
        }
        cookies = {
            'bankrotcookie': 'eea7e7c99b177fff0fd919cb96b44e9f',
            'ASP.NET_SessionId': 'wob0es3idluku2rs544nkosu'
        }
        url = f'https://bankrot.fedresurs.ru/MessageWindow.aspx?ID={guid}&attempt=1'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, cookies=cookies, headers=headers)
            return response.text
    except Exception as error:
        logger.do_write_error('error while parsing text.', error)
        return False


def parse_html_for_text(html: str = None):
    if html is None:
        return 'False'
    try:
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find('div', {'class': 'msg'}).text
        text = div.split('Текст:')[-1]
        return text
    except:
        return 'False'


def datetime_returning():
    # todo: возврат времени в соответствующем часовом поясе
    pass


def datetime_from_string(string: str) -> datetime.datetime:
    try:
        date = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        date = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%f')
    except Exception:
        date = datetime.datetime.strptime(
            '2000-01-01T00:00:00', '%Y-%m-%dT%H:%M:%S')
    finally:
        return date


if __name__ == '__main__':
    import asyncio
    a = asyncio.run(get_html('CBB97C6DB77A29ABF4C43BFB7B7C9505'))
    a = parse_html_for_text(a)
    print(a)
