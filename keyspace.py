import time
import sys
from redis import StrictRedis
import subprocess

# Get IP of Redis DB for Users via call to Docker API
# and connect to it using Python Redis API then enable all
# keyspace events and subscribe to all messages
print(sys.argv)
if(str(sys.argv[1]) == 'h'):
    ip = str(subprocess.check_output(["sudo", "docker", "inspect", "-f", "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'","socialnetwork_home-timeline-redis_1"]).strip(),'utf-8').strip("\'")
    print("Home: ",ip)
    name = 'home'
if(str(sys.argv[1]) == 'u'):
    ip = str(subprocess.check_output(["sudo", "docker", "inspect", "-f", "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'","socialnetwork_user-timeline-redis_1"]).strip(),'utf-8').strip("\'")
    print("User: ",ip)
    name = 'user'
if(str(sys.argv[1]) == 's'):
    ip = str(subprocess.check_output(["sudo", "docker", "inspect", "-f", "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'","socialnetwork_social-graph-redis_1"]).strip(),'utf-8').strip("\'")
    print("Social: ",ip)
    name = 'social'
if(str(sys.argv[1]) == 'c'):
    ip = str(subprocess.check_output(["sudo", "docker", "inspect", "-f", "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'","socialnetwork_compose-post-redis_1"]).strip(),'utf-8').strip("\'")
    print("Compose: ",ip)
    name = 'compose'

#redis = StrictRedis(host='localhost', port=6379)
redis = StrictRedis(host=ip, port=6379)
redis.config_set('maxmemory',str(sys.argv[2]))
redis.config_set('maxmemory-policy','allkeys-lru')
redis.config_set('notify-keyspace-events', 'AKEm')
pubsub = redis.pubsub()
pubsub.psubscribe('__keyspace@0__:*')

# Initialize local total tallies to 0
totalMisses = 0
totalEvictions = 0
totalZadds = 0
totalDels = 0

# Create new file with current time stamp as name
ts = str(subprocess.check_output(["date","--rfc-3339=seconds"]).strip(),'utf-8').strip("\'")
ts = ts.replace(' ','_')
ts = ts.replace(':','-')
fname = 'data/'+name+'_sub_'+ts+'.txt'
print(fname)

#Create loop that saves messages to file
print('Starting message loop')
with open(fname,'w') as file:
    file.write('key\tcommand\ttotalZadds\ttotalMisses\ttotalDeletions\ttotalEvictions\n')
    try:
        while True:
            message = pubsub.get_message()
            if message:
            # first message data is 1 which breaks the string encoder
                key = str(message ['channel'],'utf-8').split('__:')[1]
                data = str(message['data'])
                if(data != '1'):
                # Reports the database and the key that triggered the miss
                    data = str(message['data'],'utf-8')
                    if(data == 'keymiss'):
                        totalMisses = totalMisses + 1
                        print('Missed Key: ',key, "Total Misses", totalMisses)
                    if(data == 'evicted'):
                        totalEvictions = totalEvictions + 1
                        print('Evicted Key: ',key)
                    if(data=='zadd'):
                        totalZadds = totalZadds + 1
                        print('Key Set: ',key)
                    if(data == 'del'):
                        totalDels = totalDels + 1
                        print('Deleted Key: ',key)
                    print(message)
                # Save information to file
                    file.write(key)
                    file.write('\t')
                    file.write(data)
                    file.write('\t')
                    file.write(str(totalZadds))
                    file.write('\t')
                    file.write(str(totalMisses))
                    file.write('\t')
                    file.write(str(totalDels))
                    file.write('\t')
                    file.write(str(totalEvictions))
                    file.write('\n')
                else:
                    time.sleep(0.0001)

    except KeyboardInterrupt:
        print('\nEnding message loop')
