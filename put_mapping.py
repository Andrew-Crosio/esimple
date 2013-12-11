# coding=utf-8
"""Put the mapping for the Esimple application"""
from pyes import ES

from settings import INDEX_NAME


ELASTICSEARCH_INDEX_SETTINGS = {
    'analysis': {
        'analyzer': {
            'k_search': {
                'type': 'custom',
                'tokenizer': 'standard',
                'filter': ['lowercase']
            },
            'k_index': {
                'type': 'custom',
                'tokenizer': 'standard',
                'filter': ['lowercase'],
                'char_filter': ['html_strip']
            }
        }
    }
}

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


def put_mapping():
    """Put ES mapping for Esimple"""
    es_connection = ES()  # Defaults to localhost:9200

    if not es_connection.indices.exists_index(INDEX_NAME):
        print 'Creating index...'
        # Create a new index with the specified index settings
        es_connection.indices.create_index(
            INDEX_NAME,
            ELASTICSEARCH_INDEX_SETTINGS
        )

        print 'Creating mappings...'
        # Put all the documents into the ES mapping
        for document, document_mapping in DOCUMENT_MAPPINGS.iteritems():
            print '\tMapping %s...' % document
            es_connection.put_mapping(
                doc_type=document,
                mapping=document_mapping,
                indices=[INDEX_NAME]
            )

        print 'Finished!'
    else:
        print 'Not putting mapping, already exists'


if __name__ == '__main__':
    put_mapping()
