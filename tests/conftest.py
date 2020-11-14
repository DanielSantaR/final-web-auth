import pytest
from starlette.testclient import TestClient

from app.main import create_application


@pytest.fixture(scope="function")
def test_app():
    # set up
    app = create_application()

    with TestClient(app) as test_client:

        # testing
        yield test_client
