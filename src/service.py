from tools import request

import asyncio
from typing import Dict

import pprint


async def get_list_company(name: str = 'ромашка') -> Dict:
    response = await request(
        name=name,
        type_='list_company',
        )
    if response:
        response = response['pageData']
        # print(len(response))
        for company in response:
            # pprint.pprint(company)
            # pass
            # return data
    return False



async def get_list_messages(
    guid="971b80ca-06fe-4bfd-98eb-07d5aeda004b",
    ) -> Dict:
    response = await request(
        type_='list_messages',
        guid=guid,
        )
    if response:
        response = response['pageData']
        for index, events in enumerate(response):
            # if events['type'] == 'BankruptcyMessage':
            #     print(index)
            pprint.pprint(events)
            # print(len(response))
            # return data
    return False


if __name__ == '__main__':
    # asyncio.run(get_list_company())
    asyncio.run(get_list_messages())