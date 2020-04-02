import time
import sys
from redis import StrictRedis
import subprocess

# Get IP of Redis DB for Users via call to Docker API
# and connect to it using Python Redis API
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
redis = StrictRedis(host=ip, port=6379)

# Create new file with current time stamp as name
ts = str(subprocess.check_output(["date","--rfc-3339=seconds"]).strip(),'utf-8').strip("\'")
ts = ts.replace(' ','_')
ts = ts.replace(':','-')
fname = 'data/'+name+'_mon_'+ts+'.txt'
print(fname)

# Save monitor information to file as it comes in
with open(fname,'w') as file:
    file.write('timestamp\tzero\tIP\tport\ttcp\tcommand\n')
    with redis.monitor() as mon:
        try:
            for command in mon.listen():
                for val in command:
                    print(command[val],'\t',end='')
                    file.write(str(command[val]))
                    file.write('\t')
                file.write('\n')
                print('')
        except KeyboardInterrupt:
            print('\nEnding monitor loop')
