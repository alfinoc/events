from operator import attrgetter
from dateutil import parser
from urlparse import urljoin
from daterangeparser import parse as daterange
from datetime import datetime, timedelta

def join(uni):
   return u' '.join(uni)

def strippedContent(element):
   return u''.join(element.stripped_strings)

def totalStrippedContent(html, selector):
   return join(map(strippedContent, html.select(selector)))

def nonEmpty(list):
   return filter(lambda elt : len(elt) > 0, list)

"""
Each handler is passed the url of a page to scrape and the parsed HTML on that page.

Each handler returns a pair of lists:
   1. A list of events, each formatted:
      {
         'venue': '_',
         'title': '_',
         'link': '_',
         'description': [ '_', '_' ],
         'dates': [ '_', '_' ],
         'imgs': [ '_', '_' ]
      }
   2. A list of urls to recursively load and handle.

All returned urls/links should be absolute.
"""

def nwffevent(url, html):
   event = {
      'title': html.select('.topheadline h4')[0].string,
      'link': url,
      'type': 'film',
      'venue': 'Northwest Film Forum'
   }

   # Description.
   description = html.select('.cinemascolumnright .textdiv_leadin > *') + \
                 html.select('.cinemascolumnright .textdiv_prose > *')
   description = nonEmpty(map(strippedContent, description))
   event['description'] = description

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
      'title': u' '.join(info.select('#aShow')[0].stripped_strings),
      'venue': u' '.join(info.select('.aVenue')[0].stripped_strings),
      'type': 'music',
      'link': url,
      'imgs': [ urljoin(url, info.select('.aImage img')[0]['src']) ]
   }

   # Expand date range, excluding day of week and <br> (first two content elements).
   dateNodes = info.select('.aDate')
   if len(dateNodes) == 0 or len(dateNodes[0]) < 3:
      # Can't do much with no date.
      return [], []
   dateString = list(dateNodes[0].stripped_strings)[-1]
   start, end = daterange(dateString.replace('&', '-'))
   full = [ start ]
   if end:
      delta = (end - start).days
      # Be careful and don't expand date ranges bigger than a year.
      if 1 <= delta and delta <= 365:
         full.extend([ start + timedelta(days=days) for days in xrange(1, delta + 1) ])
   event['dates'] = map(lambda d : d.isoformat(), full)

   # Description.
   guests = totalStrippedContent(info, '#aGuest')
   price = totalStrippedContent(info, '.aPrice')
   notes = totalStrippedContent(info, '.aNotes')
   text = nonEmpty(map(strippedContent, html.select('.aText .aContent > *')))
   event['description'] = nonEmpty([ guests, price, notes ] + text)

   return [ event ], []

def stgcalendar(url, html):
   # TODO: Right now we don't load the next month's calendar page automatically.
   # Stop recursively expanding at one year from today's date.
   relative = [ elt['href'] for elt in html.select('a.cal_titlelink') ]
   return [], [ urljoin(url, path) for path in relative ]
