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
