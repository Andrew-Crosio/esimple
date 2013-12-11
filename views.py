# coding=utf-8
"""Esimple Views"""
from pyes import ANDFilter
from pyes import ESRangeOp
from pyes import FilteredQuery
from pyes import MatchAllFilter
from pyes import MatchAllQuery
from pyes import RangeFilter
from pyes import TermFilter
from bottle import get
from bottle import request

from settings import INDEX_NAME
from settings import es_connection


RANGE_FILTER_POSTFIX = ['gt', 'gte', 'lt', 'lte']


def _get_special_filter(key, value):
    assert key.rsplit('__', 1)[-1] in RANGE_FILTER_POSTFIX

    key, postfix = key.rsplit('__', 1)
    es_filter = RangeFilter(ESRangeOp(key, postfix, value))

    return es_filter


@get('/contacts/search/')
def search_contacts():
    filters = []

    # Add filters
    for key in request.params:
        values = request.params.getlist(key)

        if '__' in key:
            # Range queries are anything range-based (< <= >= >)
            filters.extend(_get_special_filter(key, value) for value in values)
        else:
            # TermFilter is a simple a == b comparison
            filters.extend(TermFilter(key, value) for value in values)

    if filters:
        # Join all the filters with an AND filter to require all matches
        query_filter = ANDFilter(filters)
    else:
        # A query to match everything, if no search parameters provided
        query_filter = MatchAllFilter()

    # Apply the filters against a document matching all queries
    query = FilteredQuery(MatchAllQuery(), query_filter).search()

    # Perform the search
    results = es_connection.search(
        query=query,
        doc_types=['contacts'],
        indices=[INDEX_NAME]
    )

    # Return the data
    data = {
        'total': results.total,
        'results': [result for result in results]
    }

    return data
