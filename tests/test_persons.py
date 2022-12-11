from flask.testing import FlaskClient
from tests.utils import create_person, refresh_db
from src.models.models import Person

#Test logged in
def test_get_landing_loggedIn(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    
    #Run Action
    res = client.get('/')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>TestFName's Listings</h1>"

def test_get_login_loggedIn(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    
    #Run Action
    res = client.get('/login')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>TestFName's Listings</h1>"

def test_get_signup_loggedIn(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    
    #Run Action
    res = client.get('/signup')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>TestFName's Listings</h1>"

def test_signout_loggedIn(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app

    #Run Action
    res = client.get('/signout')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"

#test functions work
def test_signout_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get('/signout')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"

def test_signup(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.post('/signup', data={
        'signupFirst': "testFSign",
        'signupLast': "testLSign",
        'signupEmail': "testSign@gmail.com",
        'signupPassword': '123123123'
    }, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert '<div>Your account was successfully created</div>'

def test_login(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    create_person('testEmail@gmail.com')
    
    #Run Action
    res = sessionless_test_app.post('/login', data={
        'loginEmail': "testEmail@gmail.com",
        'loginPassword': '123123123'
    }, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert '<div>You were successfully logged in</div>'
    assert '<h1 class="text-center">Market Place</h1>'