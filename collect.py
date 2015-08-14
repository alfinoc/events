from re import search
from bs4 import BeautifulSoup as soup
from unirest import get
from functools import partial

import handlers

router = [
   ('http://www.nwfilmforum.org/live/page/calendar', handlers.nwffcalendar),
   ('http://www.nwfilmforum.org/live/page/calendar/\d+', handlers.nwffevent),
   
   #('http://www.stgpresents.org/neptune/calendar/eventdetail/*' handlers.stgEventPage),
   #'(http://www.stgpresents.org/neptune/calendar/monthcalendar/<int:year>/<int:month>/-',
   #  handlers.stgCalendarPage)

   # Local test pages.
   ('/Users/chrisalfino/Projects/events/demo/nwff.html', handlers.nwffcalendar),
   ('/Users/chrisalfino/Projects/events/demo/lookofsilence.html', handlers.nwffevent),
]

class NoMatchError(Exception):
   pass

def match(link):
   for (rule, endpoint) in router:
      if search('\A{0}\Z'.format(rule), link):
         return endpoint
   raise NoMatchError(link)

def dummy_report(events):
   from json import dumps
   global glob
   glob = events
   print dumps(events, sort_keys=True, indent=4, separators=(',', ': '))

def dispatch(urls, report=dummy_report):
   def callback(handler, response):
      events, follow = handler(soup(response.body))
      report(events)
      dispatch(follow)

   for link in urls:
      try:
         # TODO: Should be removed in final version.
         # If it's a local file, just go ahead and read the file.
         if link.startswith('/'):
            class ResponseDummy:
               def __init__(self, file):
                  self.body = open(file)
                  print file
            partial(callback, match(link))(ResponseDummy(link))
            continue

         # Request page contents asynchronously.
         get(link, callback=partial(callback, match(link)))
      except NoMatchError as e:
         print 'Could not find handler endpoint for {0}.'.format(str(e))

dispatch(['/Users/chrisalfino/Projects/events/demo/lookofsilence.html'])
