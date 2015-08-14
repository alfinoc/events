from re import search
from bs4 import BeautifulSoup as soup
from unirest import get
from functools import partial

import config

def dummy_report(events):
   from json import dumps
   global glob
   glob = events
   print dumps(events, sort_keys=True, indent=4, separators=(',', ': '))

class NoMatchError(Exception):
   pass

def match(link):
   # TODO: make config top level, like main dispatch call below.
   for (rule, endpoint) in config.router:
      if search('\A{0}\Z'.format(rule), link):
         return endpoint
   raise NoMatchError(link)

def dispatch(urls, report=dummy_report):
   def callback(handler, url, response):
      events, follow = handler(url, soup(response.body))
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
            partial(callback, match(link))(link, ResponseDummy(link))
            continue

         # Request page contents asynchronously.
         get(link, callback=partial(callback, match(link), link))
      except NoMatchError as e:
         print 'Could not find handler endpoint for {0}.'.format(str(e))

dispatch(config.roots)