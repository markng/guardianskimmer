import urllib2, pickle
try:
    import httplib2
except ImportError:
    httplib2 = None
from errors import HTTPError

def best_fetcher():
    if httplib2:
        return CacheFetcher() # Uses an in-memory cache
    else:
        return Fetcher()

class Fetcher(object):
    "Default implementation, using urllib2"
    def get(self, url):
        try:
            u = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            raise HTTPError(e.code, e)
        headers = u.headers.dict
        return headers, u.read()

class InMemoryCache(object):
    def __init__(self):
        self._cache = {}
    
    def get(self, key):
        return self._cache.get(key)
    
    def set(self, key, value):
        self._cache[key] = value
    
    def delete(key):
        if key in self._cache[key]:
            del self._cache[key]

class CacheFetcher(object):
    "Uses httplib2 to cache based on the max-age header. Requires httplib2."
    def __init__(self, cache=None):
        if cache is None:
            cache = InMemoryCache()
        self.http = httplib2.Http(cache)
    
    def get(self, url):
        headers, response = self.http.request(url)
        if headers['status'] != '200':
            raise HTTPError(int(headers['status']), headers)
        return headers, response

class ForceCacheFetcher(object):
    "Caches every response forever, ignoring the max-age header"
    def __init__(self, fetcher=None, cache=None):
        self.fetcher = fetcher or Fetcher()
        self.cache = cache or InMemoryCache()
    
    def get(self, url):
        cached_value = self.cache.get(url)
        if cached_value:
            return pickle.loads(cached_value)
        headers, response = self.fetcher.get(url)
        self.cache.set(url, pickle.dumps((headers, response)))
        return headers, response
