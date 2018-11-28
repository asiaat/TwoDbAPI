import status
import requests


def test_get_one_query_is_OK():

    r = requests.get('http://localhost:5000/api/employee/33')
    assert r.status_code == status.HTTP_200_OK

def test_get_both_queries_are_OK():

    r = requests.get('http://localhost:5000/api/employee/3')
    assert r.status_code == status.HTTP_200_OK

def test_get_no_data_found():

    r = requests.get('http://localhost:5000/api/employee/32324')
    assert r.status_code == status.HTTP_404_NOT_FOUND

def test_get_no_data_found2():

    r = requests.get('http://localhost:5000/api/employee/dsfjg')
    assert r.status_code == status.HTTP_404_NOT_FOUND

def test_get_wrong_api_query():

    r = requests.get('http://localhost:5000/dsaf/1')
    assert r.status_code == status.HTTP_404_NOT_FOUND

def test_post_insert_data():

    url = "http://localhost:5000/api/employee/"
    data = {"LastName":"Gulliver", "FirstName":"Lemuel", "BirthDate": "1661-01-01","Email":"pole@olla.co.uk"}

    r = requests.post(url,data=data)
    assert r.status_code == status.HTTP_201_CREATED




