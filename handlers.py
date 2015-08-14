from operator import attrgetter
from util import unescape

"""
Each handler returns two lists: harvested events and follow up links.
Harvested events are thrown in the pile. Follow up links get thrown back in the
dispatcher.
{
   'venue': '_',
   'title': '_',
   'description': '_',
   'dates': [ '_', '_' ],
   'link': '_',
   'img': '_'
}
"""

def nwffevent(html):
   print 'processing event'
   print html
   event = {
      'title': html.select('.topheadline h4')[0].string
   }
   description = html.select('.textdiv_prose > *')
   event['description'] = description
   return [ event ], []

def nwffcalendar(html):
   print 'processing calendar'
   return [], map(lambda e : e['href'], html.select('.cinemascolumnright h3 a'))
