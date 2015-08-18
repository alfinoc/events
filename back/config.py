import handlers

roots = [
   'http://www.nwfilmforum.org/live/page/calendar',
   #'http://www.stgpresents.org/tickets/by-month/monthcalendar/2015/08/-'

   # Local debugging roots.
   #'/Users/chrisalfino/Projects/events/demo/stgcal.html',
   #'/Users/chrisalfino/Projects/events/demo/stgevt.html'
   #'/Users/chrisalfino/Projects/events/demo/nwff.html'
   #'/Users/chrisalfino/Projects/events/demo/lookofsilence.html',
]

rules = [
   ('http://www.nwfilmforum.org/live/page/calendar', handlers.nwffcalendar),
   ('http://www.nwfilmforum.org/live/page/calendar/\d+', handlers.nwffevent),
   ('http://www.stgpresents.org/tickets/by-month/monthcalendar/.+', handlers.stgcalendar),
   ('http://www.stgpresents.org/tickets/by-month/eventdetail/.+', handlers.stgevent),

   # Local debugging pages.
   #('/Users/chrisalfino/Projects/events/demo/stgevt.html', handlers.stgevent),
   #('/Users/chrisalfino/Projects/events/demo/stgcal.html', handlers.stgcalendar),
   #('/Users/chrisalfino/Projects/events/demo/nwff.html', handlers.nwffcalendar),
   #('/Users/chrisalfino/Projects/events/demo/lookofsilence.html', handlers.nwffevent),
]
