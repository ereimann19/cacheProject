To log the keyspace events: 

sudo python3 keyspace.py u 5m

where 'u' is to monitor the user redis database. Valid options are 'u' - user, 'h' - home, 'c' - compose, or 's' - social

and 5m is the cache size limit 5m is 5MB, and passing 0 sets an unlimited cache size

To monitor the database:

sudo python3 monitor.py u

where 'u' is to monitor the user redis database. Valid options are 'u' - user, 'h' - home, 'c' - compose, or 's' - social
