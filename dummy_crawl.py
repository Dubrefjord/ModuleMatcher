import time
import sys
import os

if sys.argv[2] == '-M':
  wfd = int(os.environ['crawler_write_fd'])
  crawler_output = os.fdopen(wfd, "w",buffering=1)

os.write(wfd,str.encode("first node\n"))
time.sleep(5)
os.write(wfd,str.encode("second node\n"))
