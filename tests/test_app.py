from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200

# TODO тут нужен мок бд, чтобы были юниттесты, но я только учусь)))
# def test_get_post():
#     response = client.get('/post')
#     assert response.status_code == 200
#
#
# def test_get_dogs():
#     response = client.get('/dogs')
#     assert response.status_code == 200
#
#
# def test_create_dog():
#     response = client.post('/dog')
#     assert response.status_code == 200
#
#
# def test_get_dog_by_pk():
#     response = client.get('/dog/{pk}')
#     assert response.status_code == 200
#
#
# def test_update_dog_by_pk():
#     response = client.patch('/dog/{pk}')
#     assert response.status_code == 200
