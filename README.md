# mun-calendar

This is a set of Python scripts for parsing and graphing course information
from [Memorial University's calendar](http://www.mun.ca/regoff/calendar).
I mostly care about Engineering courses, but things might work for other
Faculties too and pull requests are welcome.

An example use is:

```bash
$ ./graph-courses.py --format=dot -o courses.dot data/2013-2014.txt
$ dot -Tpdf -o courses.pdf courses.dot
```
