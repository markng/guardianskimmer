from openplatform.guardianapi import Client
from django.shortcuts import render_to_response
from django.conf import settings

def skim(request):
  """skim view"""
  client = Client(settings.GUARDIAN_API_KEY)
  results = client.search(q = '/technology')
  return render_to_response('skimmer/skim.html', {'articles' : results})