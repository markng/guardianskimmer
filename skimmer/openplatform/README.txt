Dependencies
============

* simplejson
* httplib2 (optional, enables caching)

Usage
=====

>>> from guardianapi import Client
>>> client = Client('my-api-key-goes-here')
>>> results = client.search(q = 'ocelots')
>>> results.count()
36
>>> for item in results:
...     print item['headline']

This will return the first ten results.

To access the filters (most popular tags) for a result set:

>>> for filter in results.filters():
...    print filter

To retrieve everything (by paginating across all pages automatically), use the
following:

>>> for item in results.all():
...     print item['headline']

This will complete faster if you ask for 50 results per page:

>>> for item in client.search(q = 'ocelots', count = 50).all():
...     print item['headline']

By default, this will sleep for one second between requesting each page of 
results. If you find yourself tripping the API's rate limit, you can increase 
the sleep duration:

>>> for item in client.search(q = 'ocelots', count = 50).all(sleep = 2):
...     print item['headline']

Some API responses include URLs to make further requests. Here's how to start
a request using URL returned from a previous API call:

>>> first_filter_url = results.filters()[0]['apiUrl']
>>> new_results = client.request(first_filter_url)
