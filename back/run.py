import config
from collect import Dispatcher, Router
from json import dumps
from sys import argv, exit

if len(argv) < 2:
   exit('Usage: python run.py <out_file>')

d = Dispatcher(Router(config.rules))

print 'Starting...'
events = d.dispatch(config.roots)
print 'Complete ({0} events found).'.format(len(events))

file(argv[1], 'w').write(
   dumps(list(events), sort_keys=True, indent=4, separators=(',', ': '))
)
