#! /usr/bin/env python
import os
import sys
import signal
import re
from IPython.kernel import KernelManager, find_connection_file

# Connection file of most recently launched kernel instance
cf_name = ''
cf = find_connection_file(cf_name)

# FIXME: this gets the wrong pid (the connected client's)
# We want the pid of the kernel to send interrupts to.
# One hacky approach is to ask the kernel to os.getpid(),
# assuming it's responsive (see vim-ipython).
pid = int(re.findall(r'kernel-(\d+)\.json', cf)[0])

# Connect to kernel
km = KernelManager(connection_file=cf)
km.load_connection_file()
client = km.client()
client.start_channels()

# Propagate SIGTERM from sublime as SIGINT to kernel
def interrupt_handler(signum, frame):
    os.kill(pid, signal.SIGINT)
    sys.exit(130)
signal.signal(signal.SIGTERM, interrupt_handler)

# Code is sent over the shell channel.
# Execution runs asynchronously in the kernel process.
code = sys.argv[1]
msg_id = client.execute(code)

# Block for a response from the kernel
reply = client.get_shell_msg()
status = reply['content']['status']
prompt = reply['content']['execution_count']

if status == 'ok':
    print 'Out [%s]: succeeded!\n' % prompt

elif status == 'error':
    sys.stderr.write('Err [%s]: failed!\n' % prompt)
    for line in reply['content']['traceback']:
        sys.stderr.write(line)
    #print reply['content']['ename']
    #print reply['content']['evalue']
sys.exit(0)
