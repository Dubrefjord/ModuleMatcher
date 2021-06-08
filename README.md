This is the wrapper module in our master's thesis. The detection module can be found at https://github.com/Dubrefjord/attack_module_sql and the crawler can be found at https://github.com/mirdeger/bw. To create a new detection module, or modify a new crawler to be used with ModuleMatcher, follow the steps outlined below.



# Matcher
Wrapper for modular black box web vulnerability scanner. Runnable with the command:

python3 match.py [relative path from match.py --> crawler module] [relative path from match.py --> detection module] [URL]

For this to work, the crawler module and the detection module must be compatible with the match.py interface. The requirements on both of them are as follows:

# Making a web crawler compatible with ModuleMatcher

An example of a crawler that has been made compatible with matcher already can be found at https://github.com/mirdeger/bw

The web crawler must be runnable with the following command:

*python3 [path to crawler] --url [URL] --matcher*

When being run in this manner, the crawler must save some file descriptors from the environment. Example from when we made Black Widow compatible with matcher (in python):
```python
\# Get file descriptors for ModuleMatcher
    if matcher:
        self.write_fd = int(os.environ['crawler_write_fd'])
        self.read_fd = int(os.environ['crawler_read_fd'])
        self.crawler_pipe_output = os.fdopen(self.write_fd, "w",buffering=1)
        self.crawler_pipe_input = os.fdopen(self.read_fd, "r",buffering=1)
```

Furthermore, the crawler must send nodes to matcher as they are found, using the pipe we saved earler (write to self.crawler_pipe_output). Black Widow utilizes a navigation graph with edges in them, so in Black Widow we simply extract the nodes (according to specification covered later) and send them over the pipe. Example from the Black Widow code:
```python
# send_node_data added by MATCHER-crew. Only run if matcher == True
def send_node_data(edge, self):

    cookies = extract_cookies_from_edge(edge)
    method = edge.value.method
    data = []
    parameters = []
    json_list = []

    for node in [edge.n1, edge.n2]: #extract param from the two nodes in the edge.
      parameters = extract_parameters(node)
      json_node_data = {"url": node.value.url,
                        "parameters": ",".join(parameters),
                        "cookies": ",".join(cookies)}
      json_list.append(json_node_data)

    if method == "form":
        data, parameters = extract_data_from_forms_in_edge(edge, self)
        json_node_data = {"url": edge.value.method_data.action,
                          "parameters": ",".join(parameters),
                          "data": ",".join(data),
                          "cookies": ",".join(cookies),
                          "method": edge.value.method_data.method}
        json_list.append(json_node_data)

    if self.matcher:
        for json_node_data in json_list:
          json_node_data = json.dumps(json_node_data)
          self.crawler_pipe_output.write(str(json_node_data))
          self.crawler_pipe_output.write('\n')
          self.crawler_pipe_output.flush()
```

The function showed above is ran every time Black Widow finds an edge in the web application (meaning a way to go from one node to the next). The important thing, however, is that the implementer finds a place in the crawler code where it can extract cookies, HTTP method, parameters and HTTP POST request data as soon as they are found.

# Making a detection module compatible with ModuleMatcher

The detection module must be runnable with the following command:

*python3 [path to detection module] [json_node]*

When the detection module receives the node, it can unpack it and proceed to use the information within however it would like.

Finally, it must print whatever results it gets to standard output (stdout).

An example of a detection module being created by wrapping an existing tool (Sqlmap) is available at https://github.com/Dubrefjord/attack_module_sql
