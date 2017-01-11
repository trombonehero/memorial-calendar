from bs4 import BeautifulSoup
import re

course_number = re.compile('[0-9W]{4} [A-Z][a-z]+')
numeric = re.compile('^[0-9]+$')
special_topics = re.compile('[0-9]{4}-[0-9]{4} [A-Z][a-z]+')



def parse_prerequisites(s, prefix):
	prereqs = []

	for x in s.split(' or '):
		for y in x.split(','):
			y = y.strip()

			if y.startswith('permission of'):
				continue

			prereqs += [ prefix + ' ' + y if numeric.match(y) else y ]

	return prereqs


# A dictionary of calendar codes, their human-readable names and functions
# that parse and format them.
_ = lambda x, _ : x
codes = {
	'AR': ('attendance', _, _),
	'CH': ('credit-hours', lambda x, _ : int(x), _),
	'CO': ('co-requisite', _, _),
	'CR': ('exclusive with', _, _),
	'LC': ('lecture hours', _, _),
	'LH': ('lab hours', _, _),
	'OR': ('other information', _, _),
	'PR': ('prerequisites', parse_prerequisites, lambda xs: ', '.join(xs)),
	'UL': ('limitations', _, _),
}


def parseHTML(calfile, prefix = 'ENGI'):
	courses = {}

	soup = BeautifulSoup(calfile, 'html.parser')

	for block in soup.find_all(class_ = 'CourseBlock'):
		for c in block.find_all(class_ = 'course'):
			number = c.find(class_ = 'courseNumber').string.strip()
			name = '%s %s' % (prefix, number)
			title = c.find(class_ = 'courseTitle').string.strip()
			description = ''.join([
				d.string.strip()
					for d in c.find(class_ = 'courseDesc').p
					if d.string is not None
			])

			if 'inactive course' in description:
				continue

			course = {
				'credit-hours': 3,
				'description': description,
				'lecture hours': 3,
				'name': name,
				'number': number,
				'title': title,
			}

			courses[name] = course

			for attr in c.find_all(class_ = 'courseAttrs'):
				content = ' '.join([
					a.string.strip()
						for a in attr
						if a.string is not None
				])

				# We can't just assign parts to (key,value) because at least
				# one calendar entry has an extra colon between the code and
				# the string value.
				parts = content.split(':')
				key = parts[0]
				value = parts[-1].strip()

				(name,parse,reformat) = codes[key]
				course[name] = parse(value, prefix)

	return courses


def parseText(calfile, prefix = 'ENGI'):
	courses = {}

	for line in calfile:
		line = line.strip()

		if special_topics.match(line):
			continue

		if course_number.match(line):
			number = line.split()[0]
			name = '%s %s' % (prefix, number)
			course = {
				'credit-hours': 3,
				'description': line[5:].strip(),
				'lecture hours': 3,
				'name': name,
				'number': number,
			}

			courses[name] = course

		else:
			parts = line.split(':')

			if len(parts) < 2:
				raise ValueError("expected 'key: val', got '%s'" % line)

			# We can't just assign parts to (key,value) because at least
			# one calendar entry has an extra colon between the code and
			# the string value.
			key = parts[0]
			value = parts[-1].strip()

			(name,parse,reformat) = codes[key]
			course[name] = parse(value, prefix)

	return courses


def pseudo_prerequisites():
	courses = {}

	for (name,prereqs) in {
	'completion of Term 3 of the Civil Engineering program':
		[ 'ENGI 3101', 'ENGI 3425', 'ENGI 3610',
		  'ENGI 3703', 'ENGI 3731', 'ENGI 3934' ],

	'completion of Academic Term 5 of the Civil Engineering program':
		[ 'ENGI 5312', 'ENGI 5434', 'ENGI 5706', 'ENGI 5713', 'ENGI 5723' ],

	# Under-specified prerequite for a Term 6 Mechanical course
	'completion of Academic Term 5':
		[ 'ENGI 4421', 'ENGI 5911', 'ENGI 5931', 'ENGI 5952', 'ENGI 6961' ],

	'completion of Academic Term 6 of the Civil Engineering program':
		[ 'ENGI 6322', 'ENGI 6705', 'ENGI 6707', 'ENGI 6713' ],

	'completion of Academic Term 6 of the Computer Engineering program':
		[ 'ENGI 6861', 'ENGI 6871', 'ENGI 6876', 'ENGI 6892' ],

	'completion of Academic Term 6 of the Electrical Engineering program':
		[ 'ENGI 6901', 'ENGI 6929', 'ENGI 6933', 'ENGI 6951' ],

	'completion of Academic Term 6 of the Mechanical Engineering program':
		[ 'ENGI 6813', 'ENGI 6843', 'ENGI 6855', 'ENGI 6871' ],

	'completion of academic term 6 of the Process Engineering program':
		[ 'ENGI 6631', 'ENGI 6651', 'ENGI 6671', 'ENGI 6901', 'ENGI 6961' ],

	# This is also basically just process engineering.
	'completion of Academic Term 6':
		[ 'ENGI 6631', 'ENGI 6651', 'ENGI 6671', 'ENGI 6901', 'ENGI 6961' ],

	'completion of Term 7 of the Civil Engineering program':
		[ 'ENGI 7102', 'ENGI 7704', 'ENGI 7713', 'ENGI 7745', 'ENGI 7748' ],
			}.items():
		courses[name] = {
			'name': name,
			'number': name,
			'prerequisites': prereqs,
		}

	return courses


def format(courses, output):
	for course in sorted(courses.values(), key = lambda c : c['number']):
		output.write('%d %s\n' % (course['number'], course['description']))

		for (code, (name,parse,reformat)) in sorted(codes.items()):
			if name in course:
				output.write('\t%s: %s\n' % (code, reformat(course[name])))
