import config
from collect import Dispatcher, Router
from json import dumps

d = Dispatcher(Router(config.rules))

print 'Starting...'
events = d.dispatch(config.roots)
print 'Complete (', len(events), ' events found).'

print dumps(list(events), sort_keys=True, indent=4, separators=(',', ': '))
