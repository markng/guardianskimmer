from openplatform.guardianapi import Client
from django.shortcuts import render_to_response
from django.utils.http import urlencode
from django.conf import settings
import datetime

def skim(request, **args):
  """skim view"""
  time = datetime.datetime.now() - datetime.timedelta(days=1)
  client = Client(settings.GUARDIAN_API_KEY)
  if args.has_key('search'):
    results = client.search(q = '/' + args['search'], after = time.strftime('%Y%m%d'))
  else:
    results = client.search(q = '', after = time.strftime('%Y%m%d'))
  return render_to_response('skimmer/skim.html', {'articles' : results})