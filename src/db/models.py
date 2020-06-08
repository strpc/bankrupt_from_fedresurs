from datetime import datetime
from typing import List

from asyncpg import Record
from pydantic import BaseModel, validator
import ujson

from config import FORMAT_DATE_TIME


class Event(BaseModel):
    bankrupt_name: str
    title: str
    number: int
    text: str
    data_publish: datetime
    guid: str

    @validator('data_publish')
    def datetime_to_string(cls, date: datetime = None) -> str:
        if date is None or isinstance(date, datetime) is not True:
            date = datetime.datetime.now()
        return date.strftime(FORMAT_DATE_TIME)

    @validator('guid')
    def build_url(cls, url: str) -> str:
        base_url = 'https://bankrot.fedresurs.ru/MessageWindow.aspx?ID='
        return base_url + url

    class Config:
        json_loads = ujson.loads
        json_dumps = ujson.dumps


class ListEvent(BaseModel):
    data: List[Event]

    class Config:
        json_loads = ujson.loads
        json_dumps = ujson.dumps