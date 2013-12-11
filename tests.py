# coding=utf-8
"""Tests for ESimple"""
from time import sleep
import operator
import requests

from put_mapping import put_mapping
from put_data import put_data
from put_data import TEST_DATA
from settings import INDEX_NAME
from settings import es_connection


def test_all():
    print 'Deleting ES index if it exists...'
    try:
        es_connection.indices.delete_index(INDEX_NAME)
    except:
        pass

    put_mapping()
    put_data()

    print 'Running tests...'

    # Sleep to ensure ES is updated
    sleep(1)

    # Test find all query
    response = requests.get('http://127.0.0.1:8080/contacts/search/')
    json_data = response.json()
    assert int(json_data['total']) == len(json_data['results']) == 50
    results = sorted(json_data['results'], key=operator.itemgetter('name'))
    test_results = sorted(TEST_DATA, key=operator.itemgetter('name'))
    assert results == test_results

    # Test array search
    response = requests.get('http://127.0.0.1:8080/contacts/search/?group=family')
    assert len(response.json()['results']) == 16
    assert all('family' in result.get('groups', []) for result in response.json()['results'])

    # Test array search with multiple values
    response = requests.get('http://127.0.0.1:8080/contacts/search/?group=family&group=friends')
    assert all('family' in result.get('groups', []) for result in response.json()['results'])
    assert all('friends' in result.get('groups', []) for result in response.json()['results'])

    # Test long comparison
    response = requests.get('http://127.0.0.1:8080/contacts/search/?age=85')
    assert response.json() == {
        u'total': 1,
        u'results': [
            {
                u'age': 85,
                u'coords': {
                    u'location': u'92.10,-29.05'
                },
                u'name': u'Najam Smith',
                u'groups': [u'friends']
            }
        ]
    }

    # Test Greater Than
    response = requests.get('http://127.0.0.1:8080/contacts/search/?age__gt=60')
    assert len(response.json()['results']) == 19
    assert all(result.get('age', 0) > 60 for result in response.json()['results'])

    # Test Less Than
    response = requests.get('http://127.0.0.1:8080/contacts/search/?age__lt=30')
    assert len(response.json()['results']) == 12
    assert all(result.get('age', 0) < 30 for result in response.json()['results'])

    print 'Success!'


if __name__ == '__main__':
    test_all()
