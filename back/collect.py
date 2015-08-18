from re import search
from bs4 import BeautifulSoup as soup
from unirest import get, timeout as setTimeout
from functools import partial
from threading import Lock, Thread, Condition
from json import dumps, loads

setTimeout(10)

class Router:
   class NoMatchError(Exception):
      pass

   def __init__(self, rules=[]):
      self.rules = rules

   def match(self, link):
      for (rule, endpoint) in self.rules:
         if search('\A{0}\Z'.format(rule), link):
            return endpoint
      raise Router.NoMatchError(link)

class Dispatcher:
   def __init__(self, router):
      self.router = router

   def report(self, events):
      self.harvested.update(map(dumps, events))
      print '{0} pending'.format(self.pending)

   def dispatch(self, urls):
      # Initialize threading and logging state.
      self.lock = Lock()
      self.cleanUp = Condition(self.lock)
      self.pending = 0
      self.seen = set()
      self.harvested = set()

      # Start with the roots.
      self._dispatch(urls)

      # Wait for dispatching to complete.
      self.cleanUp.acquire()
      while self.pending > 0:
         self.cleanUp.wait()
      self.cleanUp.release()
      return list(map(loads, self.harvested))

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
                  syncCB = partial(self._callback, self.router.match(link))
                  Thread(target=syncCB, args=(link, ResponseDummy(link))).start()
               # TODO: stop removing dummy code here.

               else:
                  # Request page contents asynchronously.
                  get(link, callback=partial(self._callback, self.router.match(link), link))

               self.seen.add(link)
               self.pending += 1

            except Router.NoMatchError as e:
               print 'Could not find handler endpoint for {0}.'.format(str(e))

   def _callback(self, handler, url, response):
      try:
         events, follow = handler(url, soup(response.body))
         self._dispatch(follow)
      except Exception as e:
         print 'Error processing url: {0}'.format(url)

      # Note: it is essentially that this decrement occurs *after* the ._dispatch
      # call above, since self.pending cannot return to 0 until ALL requests have
      # finished (harvesting is complete).
      with self.lock:
         self.report(events)
         self.pending -= 1
         if self.pending == 0:
            self.cleanUp.notify_all()
