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


async def test_post_names_202(test_cli: SanicTestClient):
    json_req = {'name': 'Петрович'}
    uri = '/v1/names/'
    post = await test_cli.post(uri, data=dumps(json_req))
    assert post.status == 202
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


async def test_get_names_not_found_404(test_cli: SanicTestClient):
    uri = '/v1/names/3556dda5-b1d3-46ed-bb46-7e2d1d312fa3'
    resp = {"message": "Data is not found. Please check 'names'"}
    get = await test_cli.get(uri)
    assert get.status == 404
    assert resp == await get.json()


async def test_get_names_invalid_uuid_400(test_cli: SanicTestClient):
    uri = '/v1/names/3556dda5'
    resp = {"message": "Invalid uuid"}
    get = await test_cli.get(uri)
    assert get.status == 400
    assert resp == await get.json()