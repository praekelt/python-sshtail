python-sshtail
==============

A simple set of Python classes to facilitate tailing of one or more files via SSH.
At the moment it only supports key-based SSH'ing.

Quick installation
------------------
Install from PyPI:

::

    > easy_install -U python-sshtail


Tailing a single file
---------------------

::

    from sshtail import SSHTailer
    from time import sleep

    # "1.2.3.4" is the IP address or host name you want to access
    tailer = SSHTailer('1.2.3.4', '/var/log/path/to/my/logfile.log')

    try:
        while 1:
            for line in tailer.tail():
                print line
            
            # wait a bit
            time.sleep(1)

    except:
        tailer.disconnect()


Tailing multiple files
----------------------

::

    from sshtail import SSHMultiTailer

    tailer = SSHMultiTailer({
        '1.2.3.4': ['/path/to/log1.log', '/path/to/log2.log'],
        '4.3.2.1': ['/path/to/log3.log'],
    })

    # will run until it receives SIGINT, after which it will
    # automatically catch the exception, disconnect from the
    # remote hosts and perform cleanup

    for host, filename, line in tailer.tail():
        print "%s:%s - %s" % (host, filename, line)



Using a custom private key
--------------------------

::

    from sshtail import SSHMultiTailer, load_dss_key

    # if no path's specified for the private key file name,
    # it automatically prepends /home/<current_user>/.ssh/
    # and for RSA keys, import load_rsa_key instead.

    tailer = SSHMultiTailer({
            '1.2.3.4': ['/path/to/log1.log', '/path/to/log2.log'],
            '4.3.2.1': ['/path/to/log3.log'],
        },
        private_key=load_dss_key('identity'))

    for host, filename, line in tailer.tail():
        print "%s:%s - %s" % (host, filename, line)




