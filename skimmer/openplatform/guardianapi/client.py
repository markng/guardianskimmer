try:
    import simplejson
except ImportError:
    from django.utils import simplejson
import urllib, urlparse, time, re, cgi
from errors import APIKeyError, ItemNotFound, URLNotRecognised
import fetchers

class Client(object):
    base_url = 'http://api.guardianapis.com/'
    # Map paths (e.g. /content/search) to their corresponding methods:
    path_method_lookup = (
        (re.compile('^/content/search$'), 'search'),
        (re.compile('^/content/tags$'), 'tags'),
        (re.compile('^/content/item/(\d+)$'), 'item'),
    )
    
    def __init__(self, api_key, fetcher=None):
        self.api_key = api_key
        self.fetcher = fetcher or fetchers.best_fetcher()
    
    def _do_call(self, endpoint, **kwargs):
        url = '%s?%s' % (
            urlparse.urljoin(self.base_url, endpoint),
            urllib.urlencode(self.fix_kwargs(kwargs), doseq=True)
        )
        try:
            headers, response = self.fetcher.get(url)
        except fetchers.HTTPError, e:
            if e.status_code == 403:
                raise APIKeyError(self.api_key, e)
            else:
                raise
        return simplejson.loads(response)
    
    def fix_kwargs(self, kwargs):
        kwargs2 = dict([ # underscores become hyphens
            (key.replace('_', '-'), value)
            for key, value in kwargs.items()
        ])
        kwargs2['format'] = 'json'
        kwargs2['api_key'] = self.api_key
        return kwargs2
    
    def search(self, **kwargs):
        json = self._do_call('/content/search', **kwargs)
        return SearchResults(self, kwargs, json)
    
    def tags(self, **kwargs):
        json = self._do_call('/content/tags', **kwargs)
        return TagResults(self, kwargs, json)
    
    def item(self, item_id):
        try:
            json = self._do_call('/content/item/%s' % item_id)
        except HTTPError, h:
            if str(h.status_code) == '404':
                raise ItemNotFound(item_id)
            else:
                raise
        return json['content']
    
    def request(self, url):
        "Start with an already constructed URL e.g. apiUrl from a response"
        bits = urlparse.urlparse(url)
        path = bits.path
        kwargs = cgi.parse_qs(bits.query)
        found_method = None
        args = tuple()
        for r, method in self.path_method_lookup:
            m = r.match(path)
            if m:
                found_method = method
                args = m.groups()
        if not found_method:
            raise URLNotRecognised(url)
        return getattr(self, found_method)(*args, **kwargs)
    
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.base_url)

class Results(object):
    client_method = None
    default_per_page = 10 # Client library currently needs to know this
    
    def __init__(self, client, kwargs, json):
        self.client = client
        self.kwargs = kwargs
        self.json = json
    
    def __iter__(self):
        return self.results()
    
    def all(self, **kwargs):
        "Iterate over all results, handling pagination transparently"
        return AllResults(self, **kwargs)
    
    def count(self):
        return 0
    
    def start_index(self):
        return 0
    
    def per_page(self):
        return self.kwargs.get('count', self.default_per_page)
    
    def __getitem__(self, key):
        return self.json[key]
    
    def results(self):
        return []
    
    def has_next(self):
        return self.start_index() + self.per_page() < self.count()
    
    def next(self):
        "Return next Results object in pagination sequence, or None if at end"
        if not self.has_next():
            return None
        method = getattr(self.client, self.client_method)
        kwargs = dict(self.kwargs)
        start_index = kwargs.get('start_index', 0)
        count = kwargs.get('count', self.default_per_page)
        # Adjust the pagination arguments
        kwargs['count'] = count
        kwargs['start_index'] = start_index + count
        return method(**kwargs)
    
    def __iter__(self):
        for result in self.results():
            yield result
    
    def __repr__(self):
        return '<%s: %d-%d/%d for %r>' % (
            self.__class__.__name__,
            self.start_index(), self.start_index() + len(self.results()), 
            self.count(), self.kwargs
        )

class SearchResults(Results):
    client_method = 'search'
    default_per_page = 10
    
    def count(self):
        return self.json['search']['count']
    
    def start_index(self):
        return self.json['search']['startIndex']
    
    def results(self):
        return self.json['search']['results']
    
    def filters(self):
        return self.json['search']['filters']

class TagResults(Results):
    client_method = 'tags'
    default_per_page = 10
    
    def count(self):
        return self.json['subjects']['count']
    
    def start_index(self):
        return self.json['subjects']['startIndex']
    
    def results(self):
        return self.json['subjects']['tags']

class AllResults(object):
    "Results wrapper that knows how to auto-paginate a result set"
    def __init__(self, results, sleep=1, debug=lambda msg: None):
        self.results = results
        self.sleep = sleep
        self.debug = debug
    
    def __iter__(self):
        results = self.results
        while results:
            self.debug(results)
            for result in results.results():
                yield result
            time.sleep(self.sleep)
            results = results.next()
    
    def __repr__(self):
        return '<%s: %d for %r>' % (
            self.__class__.__name__, self.results.count(), self.results.kwargs
        )
