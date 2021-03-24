import os
import subprocess

def start():
    print("Starting scanner")

    # The following three variables should in reality be fetched from the arguments given when starting this program
    dm_path = "/home/mirre/Documents/Masterarbete/sqlmap_interpreter.py"
    crawler_path = "/home/mirre/Documents/Masterarbete/bw/crawl.py"
    starting_url_arg = "--url http://localhost:8080/js.php/"

    dm_read_fd, crawler_write_fd = os.pipe()
    crawler_read_fd, dm_write_fd = os.pipe()

    os.environ['dm_read_fd'] =  str(dm_read_fd)
    os.environ['dm_write_fd'] = str(dm_write_fd)
    os.environ['crawler_read_fd'] = str(crawler_read_fd)
    os.environ['crawler_write_fd'] = str(crawler_write_fd)

    dm_env = os.environ.copy()
    crawler_env = os.environ.copy()

    # Create detection module (DM) process
    dm_process = subprocess.Popen(["python3", dm_path], pass_fds=[dm_read_fd, dm_write_fd], env=dm_env)  # använda bufsize?

    os.close(dm_read_fd)
    os.close(dm_write_fd)

    # start crawler process
    crawler_process = subprocess.Popen(["python3", crawler_path, starting_url_arg], pass_fds=[crawler_read_fd, crawler_write_fd], env=crawler_env)

    json_string = "{\"url\": \"http://localhost:8080/login.php\", \"parameters\": \"username,password\", \"data\": \"username=yaipzgxn,password=yaipzgxn\", \"cookies\": \"\", \"method\": \"GET\"}\n"
    os.write(crawler_write_fd, bytes(json_string.encode()))

    crawler_process.wait()
    print("ModuleMatcher: Crawler is finished !!!!!!!!!!!")

start()

#---------------------------


import os
import json

def create_sqlmap_command():

    rfd = int(os.environ['dm_read_fd'])
    wfd = int(os.environ['dm_write_fd'])

    print("DM was started !!!!!!!!!!!")

    file_object = os.fdopen(rfd, "r")
    content = file_object.readline()

    dictionary = json.loads(content)
    print("dictionary is: ")
    print(dictionary)

    print("command is: ")
    command = "sqlmap" + " -u " + dictionary["url"] # + \
                                #           " --cookie " + dictionary["cookies"] + \
                                #           " --data " + '"' + dictionary["data"] + '"' + \
                                #           " -p " + '"' + dictionary["parameters"] + '"'
    print(command)


create_sqlmap_command()
