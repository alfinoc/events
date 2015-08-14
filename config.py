import handlers

roots = [
   '/Users/chrisalfino/Projects/events/demo/stgevt.html'
   #'http://www.nwfilmforum.org/live/page/calendar',
   #'/Users/chrisalfino/Projects/events/demo/stgcal.html',
]

router = [
   ('http://www.nwfilmforum.org/live/page/calendar', handlers.nwffcalendar),
   ('http://www.nwfilmforum.org/live/page/calendar/\d+', handlers.nwffevent),
   ('http://www.stgpresents.org/tickets/by-month/monthcalendar/.+', handlers.stgcalendar),
   ('http://www.stgpresents.org/tickets/by-month/eventdetail/.+', handlers.stgevent),
   
   #('http://www.stgpresents.org/neptune/calendar/eventdetail/*' handlers.stgEventPage),
   #'(http://www.stgpresents.org/neptune/calendar/monthcalendar/<int:year>/<int:month>/-',
   #  handlers.stgCalendarPage)

   # Local test pages.
   ('/Users/chrisalfino/Projects/events/demo/stgevt.html', handlers.stgevent),
   ('/Users/chrisalfino/Projects/events/demo/stgcal.html', handlers.stgcalendar),
   ('/Users/chrisalfino/Projects/events/demo/nwff.html', handlers.nwffcalendar),
   ('/Users/chrisalfino/Projects/events/demo/lookofsilence.html', handlers.nwffevent),
]
