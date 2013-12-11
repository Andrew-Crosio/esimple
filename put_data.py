# coding=utf-8
"""Put data into Esimple"""
import json

from settings import INDEX_NAME
from settings import es_connection


TEST_DATA = [
    {"age": 83, "coords": {"location": "27.85,-59.26"}, "name": "Ahmad Walton", "groups": ["work"]},
    {"age": 55, "coords": {"location": "1.70,89.18"}, "name": "Danny Dukhan", "groups": ["work"]},
    {"age": 75, "coords": {"location": "1.74,37.43"}, "name": "Mahdi Walton", "groups": ["family"]},
    {"age": 66, "coords": {"location": "-83.12,40.75"}, "name": "Mireia Nguyen", "groups": ["work", "friends"]},
    {"age": 72, "coords": {"location": "-78.06,69.09"}, "name": "Mireia Maryland", "groups": ["friends", "work"]},
    {"age": 19, "coords": {"location": "-99.86,-82.92"}, "name": "Mary Mujika", "groups": ["acquaintances", "friends", "work"]},
    {"age": 61, "coords": {"location": "9.74,40.73"}, "name": "John Maryland", "groups": ["friends"]},
    {"age": 46, "coords": {"location": "19.07,58.04"}, "name": "Mahdi Chin", "groups": ["acquaintances", "friends"]},
    {"age": 19, "coords": {"location": "40.36,-0.18"}, "name": "John Nguyen", "groups": ["friends"]},
    {"age": 50, "coords": {"location": "-21.71,32.09"}, "name": "Mireia Khan", "groups": ["acquaintances"]},
    {"age": 55, "coords": {"location": "30.45,0.62"}, "name": "Jibran Chin", "groups": ["acquaintances"]},
    {"age": 28, "coords": {"location": "-22.67,82.99"}, "name": "Mary Al Fara", "groups": ["acquaintances"]},
    {"age": 13, "coords": {"location": "-43.91,-63.61"}, "name": "Najam Khan", "groups": ["acquaintances", "family",]},
    {"age": 70, "coords": {"location": "-75.80,-94.65"}, "name": "Andrew Walton", "groups": ["family", "friends"]},
    {"age": 30, "coords": {"location": "98.82,57.35"}, "name": "Ahmad Maryland", "groups": ["family"]},
    {"age": 82, "coords": {"location": "-45.22,-98.06"}, "name": "Andrew Smith", "groups": ["family", "acquaintances",]},
    {"age": 27, "coords": {"location": "-30.00,-65.68"}, "name": "Mahdi Al Fara", "groups": ["work", "acquaintances", "family"]},
    {"age": 24, "coords": {"location": "-70.85,47.95"}, "name": "Andrew Al Fara", "groups": ["friends", "acquaintances"]},
    {"age": 14, "coords": {"location": "-28.27,67.97"}, "name": "Mireia Chin", "groups": ["family"]},
    {"age": 19, "coords": {"location": "-7.62,22.33"}, "name": "Ahmad Khan", "groups": ["family", "work", "family"]},
    {"age": 53, "coords": {"location": "-45.04,-68.65"}, "name": "John Chin", "groups": ["acquaintances", "family",]},
    {"age": 78, "coords": {"location": "94.27,-99.99"}, "name": "Ahmad Mujika", "groups": ["work"]},
    {"age": 49, "coords": {"location": "56.68,-63.11"}, "name": "Najam Chin", "groups": ["work", "acquaintances"]},
    {"age": 75, "coords": {"location": "-86.53,50.50"}, "name": "Danny Maryland", "groups": ["acquaintances"]},
    {"age": 75, "coords": {"location": "-32.66,-18.13"}, "name": "John Mujika", "groups": ["family", "friends", "work"]},
    {"age": 41, "coords": {"location": "-21.15,38.65"}, "name": "Andrew Chin", "groups": ["family"]},
    {"age": 57, "coords": {"location": "-62.44,32.68"}, "name": "Jibran Dukhan", "groups": ["work"]},
    {"age": 54, "coords": {"location": "63.41,21.76"}, "name": "Mireia Al Fara", "groups": ["friends", "work"]},
    {"age": 44, "coords": {"location": "80.24,92.23"}, "name": "Mary Maryland", "groups": ["friends"]},
    {"age": 84, "coords": {"location": "-1.45,-40.13"}, "name": "Ahmad Dukhan", "groups": ["acquaintances"]},
    {"age": 32, "coords": {"location": "43.74,26.15"}, "name": "Jibran Khan", "groups": ["work", "acquaintances"]},
    {"age": 79, "coords": {"location": "94.46,54.71"}, "name": "Mary Chin", "groups": ["friends", "acquaintances"]},
    {"age": 35, "coords": {"location": "-70.74,-43.03"}, "name": "John Dukhan", "groups": ["work", "friends", "acquaintances"]},
    {"age": 82, "coords": {"location": "-13.57,87.40"}, "name": "Andrew Khan", "groups": ["family"]},
    {"age": 53, "coords": {"location": "-99.12,-83.35"}, "name": "Mary Dukhan", "groups": ["friends"]},
    {"age": 85, "coords": {"location": "92.10,-29.05"}, "name": "Najam Smith", "groups": ["friends"]},
    {"age": 69, "coords": {"location": "80.84,97.06"}, "name": "Mireia Walton", "groups": ["friends"]},
    {"age": 43, "coords": {"location": "-41.71,13.42"}, "name": "Jibran Nguyen", "groups": ["acquaintances", "work"]},
    {"age": 21, "coords": {"location": "67.48,-6.14"}, "name": "Ben Dukhan", "groups": ["friends"]},
    {"age": 36, "coords": {"location": "61.84,96.32"}, "name": "John Walton", "groups": ["friends", "family"]},
    {"age": 31, "coords": {"location": "-85.92,79.82"}, "name": "Andrew Dukhan", "groups": ["family"]},
    {"age": 78, "coords": {"location": "-80.22,-57.88"}, "name": "Mireia Smith", "groups": ["work"]},
    {"age": 78, "coords": {"location": "21.45,22.26"}, "name": "Danny Khan", "groups": ["acquaintances", "work"]},
    {"age": 44, "coords": {"location": "-28.31,34.21"}, "name": "Najam Nguyen", "groups": ["family", "work"]},
    {"age": 28, "coords": {"location": "46.22,20.89"}, "name": "Najam Maryland", "groups": ["acquaintances"]},
    {"age": 26, "coords": {"location": "-25.30,74.76"}, "name": "Danny Al Fara", "groups": ["friends", "acquaintances", "work"]},
    {"age": 62, "coords": {"location": "2.25,-80.33"}, "name": "Mahdi Nguyen", "groups": ["friends",]},
    {"age": 60, "coords": {"location": "-60.07,-6.26"}, "name": "John Smith", "groups": ["work", "acquaintances", "family"]},
    {"age": 62, "coords": {"location": "-75.23,-43.34"}, "name": "Jibran Mujika", "groups": ["work"]},
    {"age": 29, "coords": {"location": "20.33,79.99"}, "name": "Mary Walton", "groups": ["work"]}
]


def put_data():
    """Put ES data for Esimple"""
    print 'Putting data for {} contacts...'.format(len(TEST_DATA))
    for data in TEST_DATA:
        # Generate a hash (we don't need ID, but why not?)
        serialized_data = json.dumps(data)
        doc_id = hash(serialized_data)
        print '\tPutting: {}'.format(serialized_data)

        es_connection.index(data, INDEX_NAME, 'contacts', id=doc_id)


if __name__ == '__main__':
    put_data()
