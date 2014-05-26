#!/usr/bin/env python

import argparse
import calendar
import collections
import dot
import sys

args = argparse.ArgumentParser()
args.add_argument('filename')
args.add_argument('--format', choices = [ 'calendar', 'dot' ], default = 'dot')
args.add_argument('-o', '--output', default = '-')

args = args.parse_args()
output = sys.stdout if args.output == '-' else open(args.output, 'w')


courses = calendar.parse(open(args.filename), prefix = 'ENGI')

colours = collections.defaultdict(lambda: '#00000000')
colours[0] = '#00ffff5f'   # ONAE
colours[1] = '#00ff005f'   # The engineering profession
colours[3] = '#ff99005f'   # Mechanics and thermo
colours[4] = '#ff00ff5f'   # Math
colours[6] = '#ffff005f'   # Process
colours[7] = '#0000005f'   # Civil
colours[8] = '#0000ff5f'   # ECE
colours[9] = '#ff00005f'   # Mechanical

for course in courses.values():
	if course['name'].startswith('ENGI '):
		num = str(course['number'])
		term = int(num[0])
		department = int(num[1])

		if term == 1:
			course['colour'] = '#00000020'

		else:
			course['colour'] = colours[department]


if args.format == 'calendar':
	calendar.format(courses, output)

elif args.format == 'dot':
	dot.format(courses, output)

else:
	raise ValueError("bad output format '%s'" % args.format)
