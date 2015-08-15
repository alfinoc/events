import handlers

roots = [
   '/Users/chrisalfino/Projects/events/demo/nwff.html'
   #'http://www.stgpresents.org/tickets/by-month/eventdetail/2197/-/the-tallest-man-on-earth'
   #'/Users/chrisalfino/Projects/events/demo/stgevt.html'
   #'http://www.nwfilmforum.org/live/page/calendar',
   #'/Users/chrisalfino/Projects/events/demo/lookofsilence.html',
   #'/Users/chrisalfino/Projects/events/demo/stgcal.html',
   #'http://www.stgpresents.org/tickets/by-month/monthcalendar/2015/08/-'
   #'http://www.stgpresents.org/tickets/by-month/eventdetail/1759/-/free-neptune-tour'
   #'http://www.stgpresents.org/tickets/by-month/eventdetail/2256/-/pax'
   #'http://www.stgpresents.org/tickets/by-month/eventdetail/1965/-/gentlemen-of-the-road-stopover'

]

rules = [
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
