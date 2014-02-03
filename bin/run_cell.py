#! /usr/bin/env python
import os
import sys
import signal
import re
from IPython.kernel import KernelManager, find_connection_file

# Connection file of last opened kernel instance
code = sys.argv[1]
cf_name = ''
cf = find_connection_file(cf_name)
pid = int(re.findall(r'kernel-(\d+)\.json', cf)[0])

# Connect to kernel
km = KernelManager(connection_file=cf)
km.load_connection_file()
client = km.client()
client.start_channels()

# Propagate SIGTERM from sublime as SIGINT to kernel
def interrupt_handler(signum, frame): 
    os.kill(pid, signal.SIGINT)
    sys.exit(128+signum)
signal.signal(signal.SIGTERM, interrupt_handler)

# Code is sent over the shell channel.
# Execution runs asynchronously in the kernel process.
msg_id = client.execute(code)

# Block for a response from the kernel
reply = client.get_shell_msg()
status = reply['content']['status']
prompt = reply['content']['execution_count']

if status == 'ok':
    print 'Out [%s]: succeeded!\n' % prompt
    sys.exit(0)

elif status == 'error':        
    print 'Err [%s]: failed!\n' % prompt
    for line in reply['content']['traceback']:
        print line
    #print reply['content']['ename']
    #print reply['content']['evalue']
    sys.exit(3)

