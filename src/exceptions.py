from sanic.response import json, BaseHTTPResponse as Response
from sanic.request import Request


class APIException(Exception):
    def __init__(self, message, status, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

        self.message = message
        self.status = status

    def __str__(self):
        return f"APIException(status_code={self.status}, message={self.message})"


async def on_api_exception(request: Request, exception):
    return json(
        body={
            "error": exception.message
        },
        status=exception.status
    )
