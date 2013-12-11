# coding=utf-8
"""Put data into Esimple"""
from decimal import Decimal
import json
import random

from settings import INDEX_NAME
from settings import es_connection


DOCUMENT_MAPPINGS = {
    'contacts': {
        'properties': {
            'name': {
                'type': 'string',
            },
            'age': {
                'type': 'long'
            },
            'is_favourite': {
                'type': 'boolean'
            },
            'groups': {
                'type': 'string',
                'index_name': 'group'
            },
            'coords': {
                'type': 'geo_point'
            }
        }
    },
}

AGE_MIN = 12

AGE_MAX = 85

REQUIRED_PEOPLE = 50

GROUP_NUM_MIN = 1

GROUP_NUM_MAX = 3

COORD_QUANTIZE_LENGTH = Decimal('0.01')

GROUPS = ['family', 'friends', 'work', 'acquaintances']

FIRST_NAME_POOL = ['Andrew', 'John', 'Mary', 'Ahmad', 'Danny', 'Jibran', 'Ben', 'Najam', 'Mahdi', 'Mireia']

LAST_NAME_POOL = ['Smith', 'Maryland', 'Nguyen', 'Chin', 'Dukhan', 'Al Fara', 'Mujika', 'Khan', 'Walton']

COORD_MIN = -100

COORD_MAX = 100


def _random_coordinate():
    x_coord = Decimal(random.uniform(COORD_MIN, COORD_MAX)).quantize(COORD_QUANTIZE_LENGTH)
    y_coord = Decimal(random.uniform(COORD_MIN, COORD_MAX)).quantize(COORD_QUANTIZE_LENGTH)

    return '{},{}'.format(x_coord, y_coord)


def put_data():
    """Put ES data for Esimple"""
    print 'Generating some fake people...'
    fake_people = set()

    # Since we may get duplicates, simply create in a loop until we have enough
    while len(fake_people) < REQUIRED_PEOPLE:
        name = '%s %s' % (random.choice(FIRST_NAME_POOL), random.choice(LAST_NAME_POOL))
        fake_people.add(name)

    print 'Putting data for {} fake contacts...'.format(len(fake_people))
    for person in fake_people:
        # Compile a JSON compatible doc to put to ES with all the relevant fake information
        fake_person_data = {
            'name': person,
            'age': random.randint(AGE_MIN, AGE_MAX),
            'groups': [random.choice(GROUPS) for _ in xrange(random.randint(GROUP_NUM_MIN, GROUP_NUM_MAX))],
            'coords': {'location': _random_coordinate()}
        }

        # Generate a hash (we don't need ID, but why not?)
        serialized_data = json.dumps(fake_person_data)
        doc_id = hash(serialized_data)
        print '\tPutting: {}'.format(serialized_data)

        es_connection.index(fake_person_data, INDEX_NAME, 'contacts', id=doc_id)


if __name__ == '__main__':
    put_data()
