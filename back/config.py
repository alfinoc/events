import handlers

roots = [
   'http://www.nwfilmforum.org/live/page/calendar',
   'http://www.stgpresents.org/tickets/by-month/monthcalendar/2016/03/-',
   'http://www.stgpresents.org/tickets/by-month/monthcalendar/2016/04/-',
   #'http://www.stgpresents.org/tickets/by-month/eventdetail/2402/-/san-fermin',
   # Local debugging roots.
   #'/Users/chrisalfino/Projects/events/back/demo/stgcal.html',
   #'/Users/chrisalfino/Projects/events/back/demo/stgevt.html'
   #'/Users/chrisalfino/Projects/events/back/demo/nwff.html'
   #'/Users/chrisalfino/Projects/events/back/demo/lookofsilence.html',
]

rules = [
   ('http://www.nwfilmforum.org/live/page/calendar', handlers.nwffcalendar),
   ('http://www.nwfilmforum.org/live/page/calendar/\d+', handlers.nwffevent),
   ('http://www.stgpresents.org/tickets/by-month/monthcalendar/.+', handlers.stgcalendar),
   ('http://www.stgpresents.org/tickets/by-month/eventdetail/.+', handlers.stgevent),

   # Local debugging pages.
   #('/Users/chrisalfino/Projects/events/back/demo/stgevt.html', handlers.stgevent),
   #('/Users/chrisalfino/Projects/events/back/demo/stgcal.html', handlers.stgcalendar),
   ('/Users/chrisalfino/Projects/events/back/demo/nwff.html', handlers.nwffcalendar),
   #('/Users/chrisalfino/Projects/events/back/demo/lookofsilence.html', handlers.nwffevent),
]
