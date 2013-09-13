#! /usr/bin/env python
import sys
from IPython.kernel import find_connection_file, KernelManager

def connect_to_kernel(kernel_blob):
    cf = find_connection_file(kernel_blob)
    km = KernelManager(connection_file=cf)
    # load connection info and init communication
    km.load_connection_file()
    c = km.client()
    return c

def execute(client, code):
    # now we can run code.  This is done on the shell channel
    client.start_channels()
    print
    print "running:"

    # execution is immediate and async, returning a UUID
    msg_id = client.execute(code)

    # get_msg can block for a reply
    reply = client.get_shell_msg()

    status = reply['content']['status']
    if status == 'ok':
        print 'succeeded!'
    elif status == 'error':
        print 'failed!'
        for line in reply['content']['traceback']:
            print line

if __name__=='__main__':
	code = sys.argv[1]
	client = connect_to_kernel('') #connects to last opened instance
	execute(client, code)

