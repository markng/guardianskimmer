from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^$', 'skimmer.views.skim', {}, "home"),
  (r'^k/(?P<search>.*)$', 'skimmer.views.skim', {'type' : 'keyword'}, "skim"),
)
