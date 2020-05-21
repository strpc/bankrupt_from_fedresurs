from tools import request

import asyncio
from typing import List


async def get_list_company(name: str = None) -> List:
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


async def get_list_messages(
    guid="971b80ca-06fe-4bfd-98eb-07d5aeda004b",
) -> List:
    response = await request(
        type_='list_messages',
        guid=guid,
    )
    if response:
        response = response['pageData']
        print(type(response))
        # return response
    return False


def get_text_from_event():
    pass


if __name__ == '__main__':
    # asyncio.run(get_list_company())
    # asyncio.run(get_list_messages())
    from app import main
    main()
