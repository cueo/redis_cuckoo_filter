from rediscuckoocluster_benchmark import *
from data import keys
from random import shuffle
import timeit

shuffle(keys)
insert_data = keys[:1000]

shuffle(keys)
check_data = keys[:1000]

shuffle(keys)
remove_data = keys[:1000]

def call_insert():
	insert(insert_data)

def call_check():
	check(check_data)

def call_remove():
	remove(remove_data)

def benchmark():
	print '1000 insertions:', timeit.timeit(call_insert, number=1), 'seconds'
	print '1000 checks:', timeit.timeit(call_check, number=1), 'seconds'
	print '1000 deletions:', timeit.timeit(call_remove, number=1), 'seconds'

if __name__ == '__main__':
	benchmark()
