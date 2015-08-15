from re import search
from bs4 import BeautifulSoup as soup
from unirest import get
from functools import partial
from threading import Lock, Thread
from json import dumps

import config

def dummy_report(events):
   from json import dumps
   global glob
   glob = events
   print 'success'
   #print dumps(events, sort_keys=True, indent=4, separators=(',', ': '))

class NoMatchError(Exception):
   pass

def match(link):
   # TODO: make config top level, like main dispatch call below.
   for (rule, endpoint) in config.router:
      if search('\A{0}\Z'.format(rule), link):
         return endpoint
   raise NoMatchError(link)

class Dispatcher:
   def report(self, events):
      self.harvested.update(map(dumps, events))
      print 'success'

   def dispatch(self, urls):
      # Initialize crawl state.
      self.lock = Lock()
      self.pending = 0
      self.seen = set()
      self.harvested = set()

      # Start with the roots.
      self._dispatch(urls)

   def _dispatch(self, urls):
      with self.lock:
         for link in urls:
            # Avoid exploring the same page twice.
            if link in self.seen:
               continue

            try:
               # TODO: Should be removed in final version.
               # If it's a local file, just go ahead and read the file.
               if link.startswith('/'):
                  class ResponseDummy:
                     def __init__(self, file):
                        self.body = open(file)
                  syncCB = partial(self._callback, match(link))
                  Thread(target=syncCB, args=(link, ResponseDummy(link))).start()
               # TODO: stop removing dummy code here.

               else:
                  # Request page contents asynchronously.
                  get(link, callback=partial(self._callback, match(link), link))

               self.seen.add(link)
               self.pending += 1
               print 'spinning up. pending: {0}'.format(self.pending)

            except NoMatchError as e:
               print 'Could not find handler endpoint for {0}.'.format(str(e))

   def _callback(self, handler, url, response):
      try:
         events, follow = handler(url, soup(response.body))
         self.report(events)
         self._dispatch(follow)
      except Exception as e:
         print 'Error processing url: {0}'.format(url)
         print e

      with self.lock:
         self.pending -= 1
         print 'finishing. pending: {0}'.format(self.pending)

d = Dispatcher()
d.dispatch(config.roots)