from sanic.testing import SanicTestClient
from ujson import dumps


async def test_index_404(test_cli: SanicTestClient):
    resp_json = {"message": "path does not exist"}
    uri = '/'

    get = await test_cli.get(uri)
    assert get.status == 404
    assert await get.json() == resp_json

    post = await test_cli.post(uri)
    assert post.status == 404
    assert await post.json() == resp_json

    put = await test_cli.put(uri)
    assert put.status == 404
    assert await put.json() == resp_json

    delete = await test_cli.delete(uri)
    assert delete.status == 404
    assert await delete.json() == resp_json

    head = await test_cli.head(uri)
    assert head.status == 404

    options = await test_cli.options(uri)
    assert options.status == 404
    assert await options.json() == resp_json


async def test_v1_404(test_cli: SanicTestClient):
    resp_json = {"message": "path does not exist"}
    uri = '/v1/'

    get = await test_cli.get(uri)
    assert get.status == 404
    assert await get.json() == resp_json

    post = await test_cli.post(uri)
    assert post.status == 404
    assert await post.json() == resp_json

    put = await test_cli.put(uri)
    assert put.status == 404
    assert await put.json() == resp_json

    delete = await test_cli.delete(uri)
    assert delete.status == 404
    assert await delete.json() == resp_json

    head = await test_cli.head(uri)
    assert head.status == 404

    options = await test_cli.options(uri)
    assert options.status == 404
    assert await options.json() == resp_json


async def test_post_names_201(test_cli: SanicTestClient):
    json_req = {'name': 'Test'}
    uri = '/v1/names/'
    post = await test_cli.post(uri, data=dumps(json_req))
    assert post.status == 201
    assert 'name' in await post.json()
    assert json_req['name'] in (await post.json()).values()


async def test_post_names_400(test_cli: SanicTestClient):
    json_resp = {
        'message': "key 'name' in body json is not found. please repeat "
        "the request with the key 'name'"
        }
    uri = '/v1/names/'
    post = await test_cli.post(uri)
    assert post.status == 400
    assert json_resp == await post.json()


async def test_get_names_200(test_cli: SanicTestClient):
    pass


async def test_get_names_404(test_cli: SanicTestClient):
    pass