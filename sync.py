import time
from redis import StrictRedis
import subprocess

# Initializing input character to control loop
# and variable tracking number of sync events
inputval = 'v'
syncval = 1

# Get IP of Redis DB for all 4 via calls to Docker API
# and connect to them using Python Redis API
ip = str(subprocess.check_output(["sudo", "docker", "inspect", "-f", "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'","socialnetwork_user-timeline-redis_1"]).strip(),'utf-8').strip("\'")
r_user = StrictRedis(host=ip, port=6379)
ip = str(subprocess.check_output(["sudo", "docker", "inspect", "-f", "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'","socialnetwork_home-timeline-redis_1"]).strip(),'utf-8').strip("\'")
r_home = StrictRedis(host=ip, port=6379)
ip = str(subprocess.check_output(["sudo", "docker", "inspect", "-f", "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'","socialnetwork_compose-post-redis_1"]).strip(),'utf-8').strip("\'")
r_compose = StrictRedis(host=ip, port=6379)
ip = str(subprocess.check_output(["sudo", "docker", "inspect", "-f", "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'","socialnetwork_social-graph-redis_1"]).strip(),'utf-8').strip("\'")
r_social = StrictRedis(host=ip, port=6379)

# Create new file with current time stamp as name
ts = str(subprocess.check_output(["date","--rfc-3339=seconds"]).strip(),'utf-8').strip("\'")
ts = ts.replace(' ','_')
ts = ts.replace(':','-')
fname = 'data/sync_'+ts+'.txt'
print(fname)

# Save monitor information to file as it comes in
with open(fname,'w') as file:
    #file.write('sync')
    file.write('database')
    information = r_user.info('Memory')
    for k in information:
        file.write('\t')
        file.write(str(k))
    information = r_user.info('Stats')
    for k in information:
        file.write('\t')
        file.write(str(k))
    information = r_user.info('Keyspace')
    for k in information:
        file.write('\t')
        file.write(str(k))
    file.write('\n')
    while(inputval != 'e'):
        inputval = input('Press s to sync, e to end: ')
        if(inputval == 's'):
            message = 'sync'+str(syncval)
            r_user.set(message,0)
            r_home.set(message,0)
            r_compose.set(message,0)
            r_social.set(message,0)
            print(message)
            file.write(message)
            file.write('\n')
            file.write('user')
            information = r_user.info('Memory')
            for k in information:
                file.write('\t')
                file.write(str(information[k]))
            information = r_user.info('Stats')
            for k in information:
                file.write('\t')
                file.write(str(information[k]))
            information = r_user.info('Keyspace')
            for k in information:
                file.write('\t')
                file.write(str(information[k]))
            file.write('\n')
            file.write('home')
            information = r_home.info('Memory')
            for k in information:
                file.write('\t')
                file.write(str(information[k]))
            information = r_home.info('Stats')
            for k in information:
                file.write('\t')
                file.write(str(information[k]))
            information = r_home.info('Keyspace')
            for k in information:
                file.write('\t')
                file.write(str(information[k])) 
            file.write('\n')
            file.write('compose')
            information = r_compose.info('Memory')
            for k in information:
                file.write('\t')
                file.write(str(information[k]))
            information = r_compose.info('Stats')
            for k in information:
                file.write('\t')
                file.write(str(information[k]))
            information = r_compose.info('Keyspace')
            for k in information:
                file.write('\t')
                file.write(str(information[k])) 
            file.write('\n')
            file.write('social')
            information = r_social.info('Memory')
            for k in information:
                file.write('\t')
                file.write(str(information[k]))
            information = r_social.info('Stats')
            for k in information:
                file.write('\t')
                file.write(str(information[k]))
            information = r_social.info('Keyspace')
            for k in information:
                file.write('\t')
                file.write(str(information[k])) 
            file.write('\n')
            syncval = syncval + 1
