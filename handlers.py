from operator import attrgetter
from dateutil import parser
from urlparse import urljoin
from daterangeparser import parse as daterange
from datetime import datetime, timedelta

def totalContents(element):
   return u''.join([ unicode(s).strip() for s in element.contents ])

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
   'imgs': [ '_', '_' ]
}
"""

def nwffevent(url, html):
   event = {
      'title': html.select('.topheadline h4')[0].string,
      'link': url,
      'venue': 'Northwest Film Forum'
   }

   # Description.
   descNodes = html.select('.cinemascolumnright .textdiv_leadin > *,' +
                           '.cinemascolumnright .textdiv_prose > *')
   descNodes = filter(lambda s : len(s) > 0, map(totalContents, descNodes))
   descNodes = [ u'<p>{0}</p>'.format(s) for s in descNodes ]
   event['description'] = u''.join(descNodes)

   # Could be a whole list of dates.
   dateWrappers = html.select('.cinemascolumnright > p')
   dates = []
   for elt in dateWrappers:
      candidates = [ unicode(node.string).strip() for node in elt.contents ]
      # Exclude date range strings (redundant) and ignore empty strings, since
      # the parser treats those as today (kinda weird...).
      candidates = filter(lambda s : '-' not in s, candidates)
      candidates = filter(lambda s : len(s.strip()) > 0, candidates)
      for c in candidates:
         try:
            dates.append(parser.parse(c).isoformat())
         except:
            pass
   event['dates'] = dates

   images = html.select('.cinemascolumnleft .feature_image')
   event['imgs'] = [ urljoin(url, elt['src']) for elt in images ]
   return [ event ], []

def nwffcalendar(url, html):
   relative = [ elt['href'] for elt in html.select('.cinemascolumnright h3 a') ]
   return [], [ urljoin(url, path) for path in relative ]

def stgevent(url, html):
   info = html.select('#aInfo')[0]
   event = {
      'title': info.select('#aShow')[0].string,
      'link': url,
      'imgs': [ urljoin(url, info.select('.aImage img')[0]['src']) ]
   }

   # Description.
   guests = info.select('#aGuest')[0].string.strip()
   price = totalContents(info.select('.aPrice')[0])
   notes = info.select('.aNotes')[0].string.strip()
   text = totalContents(html.select('.aText .aContent')[0])
   desc = (guests, price, notes, text)
   event['description'] = u''.join([ u'<p>{0}</p>'.format(s) for s in desc ])

   # Expand date range, excluding day of week and <br> (first two content elements).
   start, end = daterange(info.select('.aDate')[0].contents[2])
   full = [ start ]
   if end:
      delta = (end - start).days
      # Be careful and don't expand date ranges bigger than a year.
      if 1 <= delta and delta <= 365:
         full.extend([ start + timedelta(days=days) for days in xrange(1, delta + 1) ])
   event['dates'] = map(lambda d : d.isoformat(), full)
   return [ event ], []

def stgcalendar(url, html):
   # Stop recursively expanding at one year in advance today's date.
   relative = [ elt['href'] for elt in html.select('a.cal_titlelink') ]
   return [], [ urljoin(url, path) for path in relative ]
