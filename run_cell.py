#! /usr/bin/env python
import sys
from IPython.kernel import find_connection_file, KernelManager

def connect_to_kernel(file_name):
    cf = find_connection_file(file_name)
    km = KernelManager(connection_file=cf)
    km.load_connection_file()
    return km.client()


if __name__=='__main__':
    code = sys.argv[1]
    
    client = connect_to_kernel('') #connects to last opened instance

    # now we can run code.  This is done on the shell channel
    client.start_channels()

    # execution is immediate and async, returning a UUID
    print
    print "running:"
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

