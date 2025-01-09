import pytest

from snakeeyes.app import create_app


@pytest.yield_fixture(scope="session")
def app():
    # Setup up test flask app
    params = {
        "DEBUG": False,
        "TESTING": True
    }

    _app = create_app(settings_override=params)

    # Set up app context before running tests
    context = _app.app_context()
    context.push()

    yield _app

    context.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    # Setup an app client, this gets executed for each test function.

    yield app.test_client()
