import pytest

from source.app import app


@pytest.yield_fixture
def test_app():
    """
    Application test fixture.

    :return: Sanic app
    """
    yield app


@pytest.fixture
def test_cli(loop, test_app, sanic_client):
    """
    TestClient instance for a given Sanic app.

    :return: TestClient object
    """
    return loop.run_until_complete(sanic_client(test_app))
