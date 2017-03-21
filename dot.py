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

def format(courses, output):
	output.write('''digraph {
	node [ shape = rectangle ];
	rankdir = "LR";
''')

	for course in sorted(courses.values(), key = lambda c : c['number']):
		name = course['name']
		if 'title' in course:
			title = '%s: %s' % (name, course['title'])
		else:
			title = name

		attributes = { 'label': '"%s"' % title }
		if 'colour' in course:
			attributes['style'] = 'filled'
			attributes['fillcolor'] = '"%s"' % course['colour']

		attributes = ', '.join([ ' = '.join(x) for x in attributes.items() ])

		output.write('\t"%s" [ %s ];\n' % (name, attributes))

		if 'prerequisites' in course:
			for pr in course['prerequisites']:
				output.write('\t"%s" -> "%s";\n' % (pr, name))

		output.write('\n')

	output.write('\n}\n')
