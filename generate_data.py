from random import randint
s = []
a, b = 97, 122

for i in xrange(2000):
	s.append(chr(randint(a, b)) + chr(randint(a, b)) + chr(randint(a, b)))

print 'keys = ', s
