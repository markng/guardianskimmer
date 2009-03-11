from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^$', 'skimmer.views.skim', {}, "home"),
)
