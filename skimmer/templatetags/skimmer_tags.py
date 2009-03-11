from django import template
import datetime

register = template.Library()

@register.filter(name='guardian_format_date')
def guardian_format_date(datestring):
  """takes date formatted YYYY-MM-DDTHH:MM:SS and formats it more acceptably"""
  date = datetime.datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S')
  return date.strftime('%a %d %b %Y')