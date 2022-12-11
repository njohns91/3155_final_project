import pytest

from app import app

from tests.utils import create_person, create_listing, create_comment, refresh_db
from src.models.models import Person

@pytest.fixture(scope='module')
def sessionless_test_app():
    with app.app_context():
        refresh_db()
        Person.query.delete()
        yield app.test_client()

@pytest.fixture(scope='module')
def test_app():
    with app.app_context():
        refresh_db()
        Person.query.delete()
        test_person = create_person("testEmail@gmail.com")
        wrong_person = create_person("notEmail@gmail.com")

        with app.test_client() as test_client:
            with test_client.session_transaction() as session:
                session['person'] = {
                'person_id':test_person.person_id
                }
            print(session) # will be populated SecureCookieSession
            yield test_client, test_person, wrong_person