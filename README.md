To subscribe to the keyspace events: 

sudo python3 keyspace.py u 5m

where 'u' is to monitor the user redis database. Valid options are 'u' - user, 'h' - home, 'c' - compose, or 's' - social

and 5m is the cache size limit 5m is 5MB, and passing 0 sets an unlimited cache size

To monitor the database:

sudo python3 monitor.py u

where 'u' is to monitor the user redis database. Valid options are 'u' - user, 'h' - home, 'c' - compose, or 's' - social

Each program instance creates a file in the data folder marked with the name of the database (user, home, etc), whether it is subscribing to the keyspace (sub) or monitoring the database (mon), and a timestamp of when the file was created. To end, press ctrl-c and the with loop should handle properly closing the connection and file. They are all tab-separated if you wish to analyze in excel or libre calc.

To use sync stamps:

sudo python3 sync.py

Connects to all 4 databases, and collects info on memory and keyspace for each upon the user pressing s. This info is saved in a txt file titled sync in the data folder.
