#! /usr/bin/env python
import sys

def connect_to_kernel(file_name):
    from IPython.kernel import find_connection_file, KernelManager
    cf = find_connection_file(file_name)
    km = KernelManager(connection_file=cf)
    km.load_connection_file()
    return km.client()


if __name__=='__main__':
    code = sys.argv[1]
    
    # Connect to last opened instance
    print "connecting..."
    client = connect_to_kernel('') 

    # Code is run on the shell channel
    # Execution is immediate and async
    client.start_channels()
    uuid = client.execute(code)

    # Block for a reply
    reply = client.get_shell_msg()
    status = reply['content']['status']
    
    if status == 'ok':
        prompt = reply['content']['execution_count']
        print 'Out [%s]: succeeded!' % prompt
    elif status == 'error':
        import re
        regex = re.compile('\x1b\[[0-9;]*m', re.UNICODE)
        
        print 'failed!'
        # strip the ansi color codes from the ultraTB traceback
        for line in reply['content']['traceback']:
            print regex.sub('', line)

