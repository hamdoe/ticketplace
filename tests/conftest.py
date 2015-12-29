import pytest

from ticketplace import create_app
from ticketplace.models import db


@pytest.fixture()
def testapp(request):
    app = create_app('ticketplace.settings.TestConfig')
    client = app.test_client()

    db.app = app
    db.create_all()

    def teardown():
        db.session.remove()
        db.drop_all()

    request.addfinalizer(teardown)

    return client
