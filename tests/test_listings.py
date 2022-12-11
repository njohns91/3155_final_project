from flask.testing import FlaskClient
from tests.utils import create_listing, refresh_db
from src.models.models import Listing

#test functions work
def test_get_all_listings(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person = test_app
    test_listing = create_listing(test_person.person_id)

    #Run Action
    res = client.get('/market_place')
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<p>Other</p>' in page_data
    assert f'<p>Test Item Name</p>' in page_data
    assert f'<p>$20.02</p>' in page_data

def test_get_all_listings_empty(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person = test_app

    #Run Action
    res = client.get('/market_place')
    page_data = res.data.decode()

    assert res.status_code == 200
    assert '<div class="listing-column-main">' not in page_data
    assert '<p>No listings in the market! Go to profile to start a listing </p>'

def test_get_single_listing(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)

    #Run Action
    res = client.get(f'/listing_page/{test_listing.listing_id}')
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<h2>Test Item Name</h2>' in page_data
    assert f'<img src="/static/listing_images/testImage.png" alt="Listing-img">' in page_data
    assert f'<h3>Other</h3>' in page_data
    assert f'<p>Test Listing Description</p>' in page_data
    assert f'<p class="price">$20.02</p>' in page_data
    assert f'<p class="date-posted">{test_listing.date_posted}</p>' in page_data

def test_get_single_listing_302(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app

    #Run Action
    res = client.get(f'/listing_page/8c25c406-6e4e-4945-a9f5-22fd66f1a07d')
    page_data = res.data.decode()

    assert res.status_code == 302

def test_create_listing(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    
    #Run action
    image = './static/listing_images/testImage.png'

    res = client.post('/create_listing', data={
        'product_title': "Test Item Name",
        'product_description': 'Test Listing Description',
        'product_category': "Other",
        'product_price': 20.02,
        'product_image': (open(image, 'rb'), image)
    }, follow_redirects=True)
    
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<h2>Test Item Name</h2>' in page_data
    assert f'<img src="/static/listing_images/{test_person.person_id}-._static_listing_images_testImage.png" alt="Listing-img">' in page_data
    assert f'<h3>Other</h3>' in page_data
    assert f'<p>Test Listing Description</p>' in page_data
    assert f'<p class="price">$20.02</p>' in page_data

def test_create_listing_error(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    
    #Run action
    image = './static/listing_images/testImage.png'

    res = client.post('/create_listing', data={
        'product_description': 'Test Listing Description',
        'product_category': "Other",
        'product_price': 20.02,
        'product_image': (open(image, 'rb'), image)
    }, follow_redirects=True)
    
    page_data = res.data.decode()

    assert res.status_code == 200
    assert '<form name="create_form" action="/create_listing" method="post" enctype="multipart/form-data">' in page_data

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

def test_delete_listing(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)

    #Run Action
    res = client.get(f'/delete_listing/{test_listing.listing_id}')
    page_data = res.data.decode()

    listings = Listing.query.all()

    assert res.status_code == 302
    assert listings == []

def test_delete_listing_none(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app

    #Run Action
    res = client.get(f'/delete_listing/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert '<div class="error">Post doesnt exist</div>'
    assert "<h1>TestFName's Listings</h1>"

def test_delete_listing_not_owner(test_app: FlaskClient):
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(wrong_person.person_id)

    #Run Action
    res = client.get(f'/delete_listing/{test_listing.listing_id}')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert test_listing

#Test Not logged in
def test_market_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get('/market_place')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"

def test_listing_page_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get('/listing_page/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"

def test_create_listing_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get('/create_listing')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"

def test_update_listing_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get('/update_listing/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"

def test_delete_listing_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get('/delete_listing/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"

def test_search_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.post('/search')
    page_data = res.data.decode()

    assert res.status_code == 302
    assert "<h1>Welcome</h1>"
