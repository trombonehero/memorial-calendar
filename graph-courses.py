#!/usr/bin/env python

# Copyright 2014, 2017 Jonathan Anderson
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import argparse
import calendar as cal
import collections
import dot
import sys

args = argparse.ArgumentParser()
args.add_argument('filename', nargs = '+')
args.add_argument('--format', choices = [ 'calendar', 'dot' ], default = 'dot')
args.add_argument('-o', '--output', default = '-')

args = args.parse_args()
output = sys.stdout if args.output == '-' else open(args.output, 'w')


courses = collections.defaultdict(dict)
courses.update(cal.pseudo_prerequisites())

for filename in args.filename:
	f = open(filename)
	html = filename.endswith('.htm') or filename.endswith('.html')
	parse = cal.parseHTML if html else cal.parseText

	for (name,c) in parse(open(filename), prefix = 'ENGI').items():
		courses[name].update(c)

print(courses)
