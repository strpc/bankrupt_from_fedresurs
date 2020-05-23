import uuid
import httpx

from typing import Union
import datetime


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def uuid_from_str(data: str = None) -> uuid.UUID:
    if data is None:
        return False
    return uuid.UUID(data)


async def request(
    name: str = None,
    # method: Any['get', 'post'] = 'get',
    type_: Union['list_company', 'list_events'] = None,
    guid: str = None
    ) -> httpx.Response.json:
    """
    HTTP-запросы к сервису.

    :param str name: имя компании для поиска.
    :param str type_: тип запроса(запрос списка компаний или списка сообщений).
    :return dict:
    """
    if type_ not in ('list_company', 'list_events'):
        return False

    if type_ == 'list_company' and isinstance(name, str):
        url = 'https://fedresurs.ru/backend/companies/search'
        data = {
            "entitySearchFilter": {
            "onlyActive": True,
            "startRowIndex": 0,
            "pageSize": 100000,
            "name": name,
            # "regionNumber": None,
            # "code": None,
            # "legalCase": None
            },
            # "isCompany": None,
            # "isFirmBankrupt": None,
            # "isSro": None,
            # "isFirmTradeOrg": None,
            # "isSroTradePlace": None,
            # "isTradePlace": None
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
        # 'pragma': "no-cache",
        # 'cache-control': "no-cache",
        # 'sec-fetch-dest': "empty",
        # 'sec-fetch-mode': "cors",
        # 'sec-fetch-site': "same-origin",
        # 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)"
        # "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
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

#         searchAmReport: true
# searchFirmBankruptMessage: true
# searchFirmBankruptMessageWithoutLegalCase: false
# searchSfactsMessage: false
# searchSroAmMessage: false
# searchTradeOrgMessage: false
# sfactMessageType: null
# sfactsMessageTypeGroupId: null
# startDate: null

        headers = {
            'accept': "application/json, text/plain, */*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            'referer': "https://fedresurs.ru/company/971b80ca-06fe-4bfd-98eb-07d5aeda004b",
            'content-type': "application/json"
            # 'cookie': "fedresurscookie=e3ce631eff4f6484a13cec2f9d2f3680",
            # 'cache-control': "no-cache",
            # 'content-length': "455",
            # 'origin': "https://fedresurs.ru",
            # 'sec-fetch-dest': "empty",
            # 'sec-fetch-mode': "cors",
            # 'sec-fetch-site': "same-origin",
            # 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
            # "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            }
    else:
        return False

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        return response.json()
        # print(r.status_code)
        # print(len())


def get_text(url):
    # todo: by selenium
    pass

def datetime_returning():
    # todo: возврат времени в соответствующем часовом поясе
    pass

def datetime_from_string(string: str) -> datetime.datetime:
    try:
        date = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        date = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%f')
    except Exception:
        date = datetime.datetime.strptime('2000-01-01T00:00:00', '%Y-%m-%dT%H:%M:%S')
    finally:
        return date


if __name__ == '__main__':
    pass
    # import asyncio
    # asyncio.run(test_req())
#     asyncio.run(request(name='ромашка', type_='list_events'))

