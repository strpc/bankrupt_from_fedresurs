from tools import request

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


async def get_list_events(guid: str = None) -> List:
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


def get_text_from_event():
    pass