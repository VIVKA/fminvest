import pytest
# from mock import MagicMock
# from sqlalchemy.sql import text
from app import create_app


@pytest.fixture
def app(request):
    app = create_app('test')

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app
