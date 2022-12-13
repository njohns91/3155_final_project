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
    print(page_data)
    assert res.status_code == 200
    assert f'<p><a href="/profile/{test_person.person_id}">TestFName TestLName</a>:</p>' in page_data
    assert f'<p class="comment-text">Test Comment</p>' in page_data

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
    assert f'<p><a href="/profile/{test_person.person_id}">TestFName TestLName</a>:</p>' in page_data1
    assert f'<p class="comment-text">Test Comment</p>' in page_data1
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
    assert f'<p><a href="/profile/{test_person.person_id}">TestFName TestLName</a>:</p>' in page_data
    assert f'<p class="comment-text">Test Comment</p>' in page_data

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

def test_update_comment_get(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    test_comment = create_comment(test_person.person_id, test_listing.listing_id)

    #Run Action
    res = client.get(f'/update_comment/{test_listing.listing_id}/{test_comment.comment_id}')
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<form class="input-group mb-3" method = "POST" action="/update_comment/{test_listing.listing_id}/{test_comment.comment_id}">' in page_data
    assert '<input type="text" id="text" name="text" class="form-control" value="Test Comment">' in page_data
    assert '<button type="submit" class="btn btn-primary">Update</button>' in page_data

def test_update_comment_get_not_Owner(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(wrong_person.person_id)
    test_comment = create_comment(wrong_person.person_id, test_listing.listing_id)

    #Run Action
    res = client.get(f'/update_comment/{test_listing.listing_id}/{test_comment.comment_id}')

    assert res.status_code == 302

def test_update_comment_get_no_Comment(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)

    #Run Action
    res = client.get(f'/update_comment/{test_listing.listing_id}/571158c5-c1ad-4445-9552-99b109882b21')

    assert res.status_code == 302

def test_update_comment_get_no_Listing(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app

    #Run Action
    res = client.get(f'/update_comment/571158c5-c1ad-4445-9552-99b109882b21/571158c5-c1ad-4445-9552-99b109882b21')

    assert res.status_code == 302

def test_update_comment(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    test_comment = create_comment(test_person.person_id, test_listing.listing_id)

    #Run Action
    res = client.post(f'/update_comment/{test_listing.listing_id}/{test_comment.comment_id}', data={
        'text': "Test Comment Updated"
    }, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<p><a href="/profile/{test_person.person_id}">TestFName TestLName</a>:</p>' in page_data
    assert '<p class="comment-text">Test Comment Updated</p>'in page_data

def test_update_comment_no_text(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)
    test_comment = create_comment(test_person.person_id, test_listing.listing_id)

    #Run Action
    res = client.post(f'/update_comment/{test_listing.listing_id}/{test_comment.comment_id}', data={}, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<div class="error">Comment cannot be empty.</div>' in page_data
    assert f'<p><a href="/profile/{test_person.person_id}">TestFName TestLName</a>:</p>' in page_data
    assert '<p class="comment-text">Test Comment</p>'in page_data

def test_update_comment_not_Owner(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(wrong_person.person_id)
    test_comment = create_comment(wrong_person.person_id, test_listing.listing_id)

    #Run Action
    res = client.post(f'/update_comment/{test_listing.listing_id}/{test_comment.comment_id}', data={
        'text': "Test Comment Updated"
    }, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<div class="error">You cannot update comment</div>' in page_data
    assert '<p class="comment-text">Test Comment</p>'in page_data

def test_update_comment_no_Comment(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app
    test_listing = create_listing(test_person.person_id)

    #Run Action
    res = client.post(f'/update_comment/{test_listing.listing_id}/571158c5-c1ad-4445-9552-99b109882b21', data={
        'text': "Test Comment Updated"
    }, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<div class="error">Comment does not exist</div>' in page_data

def test_update_comment_no_Listing(test_app: FlaskClient):
    #Setup
    refresh_db()
    client, test_person, wrong_person= test_app

    #Run Action
    res = client.get(f'/update_comment/571158c5-c1ad-4445-9552-99b109882b21/571158c5-c1ad-4445-9552-99b109882b21', data={
        'text': "Test Comment Updated"
    }, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<div class="error">Listing does not exsit</div>' in page_data

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

def test_update_comment_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get('/update_comment/a4561e25-efc2-4c91-af46-add1cdb1cf95/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()

    assert res.status_code == 302

def test_delete_comment_notLoggedIn(sessionless_test_app: FlaskClient):
    #Setup
    refresh_db()
    
    #Run Action
    res = sessionless_test_app.get(f'/delete_comment/a4561e25-efc2-4c91-af46-add1cdb1cf95/a4561e25-efc2-4c91-af46-add1cdb1cf95')
    page_data = res.data.decode()

    assert res.status_code == 302
