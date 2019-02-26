from rediscluster import StrictRedisCluster

startup_nodes = [{"host": "127.0.0.1", "port": "30001"}, {"host": "127.0.0.1", "port": "30002"}, {"host": "127.0.0.1", "port": "30003"}]

# Note: decode_responses must be set to True when used with python3
rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

CUCKOO_FILTER_SIZE = '10'
NODES = 3
filters = ['a', 'b', 'c']

def hash_function(key):
	'''
	# A hash function to hash the keys to a particular node.
	# Here, we are adding the ascii values of all the keys mod NODES to get the node location.
	# Consequently, if the keys are longer, the performance will suffer.
	# This logic is only temporary and really basic, and needs to be replaced.
	'''
	val = 0
	for i in key:
		val += ord(i)
	return val % NODES

def create():
	'''
	# Creating NODES cuckoo filters in all the NODES nodes.
	# The entire thing only works for 3 nodes right now, adding or removing a node might mess up the entire logic.
	# This is because of the use of consistent hashing.
	# The filter names are chosen in such a way that they go to different nodes, b => node1, c => node2, a => node3.
	# Size of each filter = CUCKOO_FILTER_SIZE.
	'''
	for filter_name in filters:
		cmd = ['cuckoocreate', filter_name, CUCKOO_FILTER_SIZE]
		try:
			print rc.execute_command(*cmd)
		except Exception as e:
			print 'Error:', e

def insert(keys):
	'''
	# Inserting elements in the cuckoo filters.
	# Each key is hashed to one of the three filters.
	# This might lead to one of the filters filling up before the other filters.
	'''
	for key in keys:
		hash_value = hash_function(key)
		if hash_value == 0:
			filter_name = 'b'
		elif hash_value == 1:
			filter_name = 'c'
		else:
			filter_name = 'a'
		cmd = ['cuckooinsertelement', filter_name, key]
		try:
			rc.execute_command(*cmd)
		except Exception as e:
			print 'Error:', e

def check(keys):
	'''
	# We are using a similar logic for checking element.
	# We only check in that cuckoo filter to which the key hashes to.
	'''
	for key in keys:
		hash_value = hash_function(key)
		if hash_value == 0:
			filter_name = 'b'
		elif hash_value == 1:
			filter_name = 'c'
		else:
			filter_name = 'a'
		cmd = ['cuckoocheckelement', filter_name, key]
		try:
			rc.execute_command(*cmd)
		except Exception as e:
			print 'Error:', e

def remove(keys):
	'''
	# Again, we use the same logic of consistent hashing to delete elements.
	'''
	for key in keys:
		hash_value = hash_function(key)
		if hash_value == 0:
			filter_name = 'b'
		elif hash_value == 1:
			filter_name = 'c'
		else:
			filter_name = 'a'
		cmd = ['cuckooremoveelement', filter_name, key]
		try:
			rc.execute_command(*cmd)
		except Exception as e:
			print 'Error:', e

def delete():
	'''
	# Logic to delete all the cuckoo filters.
	'''
	for filter_name in filters:
		cmd = ['del', filter_name]
		if rc.execute_command(*cmd) == 1:
			print 'Filter deleted.'
		else:
			print 'Filter does not exist!'

'''
# If this file is executed as a standalone, we create a client which is a wrapper around the actual redis client.
# We take the command as a string input and use it to call the actual redis commands.
'''
if __name__ == '__main__':
	while True:
		line = raw_input('>>> ')
		keys = line.split()

		if len(keys) == 1:
			if line[6:12] == 'create':
				create()

			elif line[0] == 'd':
				delete()

			elif line == 'exit':
				print 'Bu-bye!'
				exit()
			else:
				print 'Wrong command, try again!'

		else:
			keys = line.split()[1:]
			if line[6:12] == 'insert':
				insert(keys)

			elif line[6:11] == 'check':
				check(keys)

			elif line[6:12] == 'remove':
				remove(keys)

			else:
				print 'Wrong command, try again!'
