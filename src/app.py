from sanic import Sanic
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse as Response

import views
import logger
# from config


app = Sanic(__name__)
app.blueprint(views.names)
app.add_route(
    handler=views.index,
    uri='/',
    methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'],
    name='index',
    )


def main():
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        auto_reload=False,
    )


if __name__ == '__main__':
    main()