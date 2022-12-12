from flask.testing import FlaskClient
from tests.utils import create_listing, create_comment, refresh_db
from src.models.models import Listing
from src.repositories.comment_repository import comment_repository_singleton


#test functions work
def test_get_comments(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    test_comment = create_comment(test_person.person_id, test_listing.listing_id)

    #Run Action
    res = client.get(f'/listing_page/{test_listing.listing_id}')
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<p><a href="/profile/{test_person.person_id}">TestFName TestLName </a>: Test Comment</p>' in page_data

def test_get_comments_right_post(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing_1 = create_listing(test_person.person_id)
    test_listing_2 = create_listing(test_person.person_id)
    test_comment = create_comment(test_person.person_id, test_listing_1.listing_id)

    #Run Action
    res1 = client.get(f'/listing_page/{test_listing_1.listing_id}')
    page_data1 = res1.data.decode()
    res2 = client.get(f'/listing_page/{test_listing_2.listing_id}')
    page_data2 = res2.data.decode()

    assert res1.status_code == 200
    assert f'<p><a href="/profile/{test_person.person_id}">TestFName TestLName </a>: Test Comment</p>' in page_data1
    assert res2.status_code == 200
    assert f'<p>No Comments</p>' in page_data2

def test_create_comments(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    
    #Run action
    res = client.post(f'/create_comment/{test_listing.listing_id}', data={
        'text': "Test Comment"
    }, follow_redirects=True)
    
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<p><a href="/profile/{test_person.person_id}">TestFName TestLName </a>: Test Comment</p>' in page_data

def test_create_comment_no_text(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    
    #Run action
    res = client.post(f'/create_comment/{test_listing.listing_id}', data={}, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<div class="error">Comment cannot be empty.</div>' in page_data
    assert f'<p>No Comments</p>' in page_data

def test_create_comments_no_listing(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    
    #Run action
    res = client.post(f'/create_comment/a4561e25-efc2-4c91-af46-add1cdb1cf95', data={
        'text': "Test Comment"
    }, follow_redirects=True)
    
    page_data = res.data.decode()

    assert res.status_code == 200
    assert '<div class="error">Post doesnt exist</div>'
    assert "<h1>TestFName's Listings</h1>"

""" 
def test_update_listing(test_app: FlaskClient):
    #Setup
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    
    #Run action
    image = './static/listing_images/water_bottle.jpg'

    res = client.post(f'/update_listing/{test_listing.listing_id}', data={
        'product_title': "Test Item Name Update",
        'product_description': 'Test Listing Description Update',
        'product_category': "Books",
        'product_price': 22.22,
        'product_image': (open(image, 'rb'), image)
    }, follow_redirects=True)
    
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<h2>Test Item Name Update</h2>' in page_data
    assert f'<img src="/static/listing_images/{test_person.person_id}-._static_listing_images_water_bottle.jpg" alt="Listing-img">' in page_data
    assert f'<h3>Books</h3>' in page_data
    assert f'<p>Test Listing Description Update</p>' in page_data
    assert f'<p class="price">$22.22</p>' in page_data

def test_update_listing_error(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    
    #Run action
    image = './static/listing_images/testImage.png'

    res = client.post(f'/update_listing/{test_listing.listing_id}', data={
        'product_title': "Test Item Name Update",
        'product_description': '',
        'product_category': "Books",
        'product_price': 22.22,
        'product_image': (open(image, 'rb'), image)
    }, follow_redirects=True)
    
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<form name="update_form" action="/update_listing/{test_listing.listing_id}" method="post" enctype="multipart/form-data">' in page_data

def test_update_listing_none(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app

    #Run action
    image = './static/listing_images/water_bottle.jpg'

    res = client.post(f'/update_listing/a4561e25-efc2-4c91-af46-add1cdb1cf95', data={
        'product_title': "Test Item Name Update",
        'product_description': 'Test Listing Description Update',
        'product_category': "Books",
        'product_price': 22.22,
        'product_image': (open(image, 'rb'), image)
    }, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert '<div class="error">Post doesnt exist</div>'
    assert "<h1>TestFName's Listings</h1>"

def test_update_listing_not_owner(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(wrong_person.person_id)
    
    #Run action
    image = './static/listing_images/milk.webp'

    res = client.post(f'/update_listing/{test_listing.listing_id}', data={
        'product_title': "Wrong",
        'product_description': 'Wrong',
        'product_category': "Books",
        'product_price': 1.11,
        'product_image': (open(image, 'rb'), image)
    }, follow_redirects=True)
    
    page_data = res.data.decode()

    assert res.status_code == 200
    assert "<h1>TestFName's Listings</h1>" in page_data
"""
def test_delete_comment(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    test_comment = create_comment(test_person.person_id, test_listing.listing_id)
    
    #Run action
    res = client.get(f'/delete_comment/{test_listing.listing_id}/{test_comment.comment_id}')
    page_data = res.data.decode()

    comments = comment_repository_singleton.get_listing_comments(test_listing.listing_id)

    assert res.status_code == 302
    assert comments == []

def test_delete_comment_no_comment(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    test_comment = create_comment(test_person.person_id, test_listing.listing_id)
    
    #Run action
    res = client.get(f'/delete_comment/{test_listing.listing_id}/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()
    
    assert res.status_code == 302
    assert f'<p>You should be redirected automatically to the target URL: <a href="/listing_page/{test_listing.listing_id}">/listing_page/{test_listing.listing_id}</a>. If not, click the link.' in page_data

def test_delete_comment_no_listing(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    
    #Run action
    res = client.get(f'/delete_comment/a4561e25-efc2-4c91-af46-add1cdb1cf95/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()
    
    assert res.status_code == 302
    assert f'<p>You should be redirected automatically to the target URL: <a href="/market_place">/market_place</a>. If not, click the link.' in page_data

def test_delete_comment_not_owner(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    test_comment = create_comment(wrong_person.person_id, test_listing.listing_id)
    
    #Run action
    res = client.get(f'/delete_comment/{test_listing.listing_id}/{test_comment.comment_id}')
    page_data = res.data.decode()

    comment = comment_repository_singleton.get_single_comment(test_comment.comment_id)

    assert res.status_code == 302
    assert comment

#Test Not logged in
def test_create_comment_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.post('/create_comment/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"
"""
def test_update_comment_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get('/update_comment/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"
"""
def test_delete_comment_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get(f'/delete_comment/a4561e25-efc2-4c91-af46-add1cdb1cf95/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"

    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.post('/search')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"
