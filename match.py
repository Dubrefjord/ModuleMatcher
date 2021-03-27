#Mål: input match [kod med crawl()] [kod med attack()] URL
import sys
import os
import subprocess
import threading
#import time

def attack_node(json):
  print("starting attack in wrapper")
  #thread?
  attack = subprocess.run(['python3',str(attack_script), json], capture_output=True, text=True) #run ok because can wait until finish before comms.
  if attack.returncode==0:
    print(attack.args)
    print(attack.stdout)
  else:
    print("ERROR OCCURED IN ATTACKSCRIPT FOR NODE")
    print(attack.args)
    print(attack.stderr)

#tim = time.time()

dir_path = os.path.dirname(os.path.realpath(__file__))
#TODO test whether these exist or something. Use ArgumentParser like in bw Crawl
crawl_script = dir_path+'/'+sys.argv[1]
attack_script = dir_path+'/'+sys.argv[2]
url = sys.argv[3]
print("Wrapper running")
node_file = open("node_file.txt","a")

#Skapa pipes för kommunikation crawl --> MM
matcher_read_fd, crawler_write_fd = os.pipe()
crawler_read_fd, matcher_write_fd = os.pipe() #This currently isn't used, could probably remove in future. Not sure if it's possible to pass a dummy-value to pass_fds below.
os.environ['matcher_read_fd'] = str(matcher_read_fd)
os.environ['matcher_write_fd']= str(matcher_write_fd)
os.environ['crawler_write_fd'] = str(crawler_write_fd)
os.environ['crawler_read_fd']= str(crawler_read_fd)
crawler_env = os.environ.copy()

print("starting crawler")
crawler = subprocess.Popen(['python3',str(crawl_script) ,"--url" ,url, '--matcher'], pass_fds=[crawler_read_fd, crawler_write_fd], env=crawler_env, stdout=subprocess.DEVNULL) #try with stdin
os.close(crawler_read_fd)
os.close(crawler_write_fd)

crawler_output = open(matcher_read_fd,'r')
threads = []

for line in crawler_output:
  node_file.write(line)
  # TODO gör nedan i tråd!
  t= threading.Thread(target=attack_node, args=[line])
  t.start()
  threads.append(t)

node_file.close()
for thread in threads:
  thread.join()

#print(time.time() - tim)

  # # TODO:
    # Check whether we can collect something else than stdout-> PIPE. Would be nice to print only intended data to match.py
    #Attacks in separate threads so that the slow sqlmap scripts can be run concurrently.
