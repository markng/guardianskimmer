from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
import skimmer.views

urlpatterns = patterns('',
  (r'^$', cache_page(skimmer.views.skim, 600), {}, "home"),
  (r'^s/k/(?P<search>.*)$', cache_page(skimmer.views.skim, 600), {'type' : 'keyword', 'snippet' : True}, "skimsnip"),  
  (r'^k/(?P<search>.*)$', cache_page(skimmer.views.skim, 600), {'type' : 'keyword', 'snippet' : False}, "skim"),
)
