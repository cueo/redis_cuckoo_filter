# Python wrapper for Cuckoo Cluster on Redis

Requirements
------------
	% pip install redis-py-cluster

How to run
----------
To work with a pseudo client:

	% python rediscuckoocluster.py

Pseudo client operations:

	% cuckoocreate
	% reset
	% cuckooinsert key1 key2 key3
	% cuckoocheck key1 key3 key5
	% cuckooremove key1 key2
	% cuckoocheck key1 key3
	% delete

Note: no need to explicitly use `cuckoocreate` when using reset

To execute the commands:

	% from rediscuckoocluster import *

Creating cuckoo filters across the nodes:

	% create()

Inserting `keys` (where `keys` is a list of keys):

	% insert(keys)

Checking if the `keys` are present in any filter:

	% check(keys)

Deleting 'keys':

	% remove(keys)

Deleting all the cuckoo filters:

	% delete()

Reset and start anew:

	% reset()

Benchmark
---------
	% python generate_data.py
	% python test.py
