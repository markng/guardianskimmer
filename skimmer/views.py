from openplatform.guardianapi import Client
from django.shortcuts import render_to_response
from django.utils.http import urlencode
from django.conf import settings

def skim(request, **args):
  """skim view"""
  client = Client(settings.GUARDIAN_API_KEY)
  if args.has_key('search'):
    results = client.search(q = '/' + args['search'])
  else:
    results = client.search(q = '')
  return render_to_response('skimmer/skim.html', {'articles' : results})