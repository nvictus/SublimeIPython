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
    client.start_channels()

    # Execution is async
    uuid = client.execute(code)

    # Block for a reply
    reply = client.get_shell_msg()

    status = reply['content']['status']
    prompt = reply['content']['execution_count']
    if status == 'ok':
        sys.stdout.write('Out [%s]: succeeded!' % prompt)

    elif status == 'error':        
        sys.stdout.write('Err [%s]: failed!' % prompt)
        for line in reply['content']['traceback']:
            sys.stderr.write(line)