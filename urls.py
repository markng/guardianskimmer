from django.conf.urls.defaults import *
from django.conf import settings
from os import path as os_path


urlpatterns = patterns('',
  ( r'^stylesheets/(.*)$', 
    'django.views.static.serve', 
    {'document_root': os_path.join(settings.PROJECT_PATH, 'media/stylesheets')}, 
    'stylesheets'
  ),
  ( r'^javascript/(.*)$', 
    'django.views.static.serve', 
    {'document_root': os_path.join(settings.PROJECT_PATH, 'media/javascript')}, 
    'javascript'
  ),
  (r'^', include('skimmer.urls')),
)
