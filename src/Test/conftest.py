from os.path import abspath
import sys
sys.path.append(abspath('../'))

import pytest
from app import app as my_app


@pytest.yield_fixture
def app():
    yield my_app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))