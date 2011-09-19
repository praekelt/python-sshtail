#
# Library to handle tailing of files via SSH.
#
# thane@praekelt.com
#

import os
import time
import paramiko


class SSHTailer(object):
    """
    Class to handle the tailing of a single file via SSH.
    """

    def __init__(self, host, remote_filename, private_key=None, verbose=False):
        if '@' in host:
            self.username, self.host = tuple(host.split('@'))
        else:
            self.username, self.host = None, host
        self.remote_filename = remote_filename
        self.private_key = private_key
        self.client = None
        self.sftp_client = None
        self.remote_file_size = None
        self.line_terminators = ['\r', '\n', '\r\n']
        self.line_terminators_joined = '\r\n'

        self.verbose = verbose


    def connect(self):
        if self.verbose:
            print "Connecting to %s..." % self.host
        # connect to the host
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.private_key:
            self.client.connect(self.host, username=self.username, pkey=self.private_key)
        else:
            self.client.connect(self.host, username=self.username)

        if self.verbose:
            print "Opening remote file %s..." % self.remote_filename
        # open a connection to the remote file via SFTP
        self.sftp_client = self.client.open_sftp()
        


    def tail(self):
        # make sure there's a connection
        if not self.sftp_client:
            self.connect()

        fstat = self.sftp_client.stat(self.remote_filename)

        # check if we have the file size
        if self.remote_file_size is not None:
            # if the file's grown
            if self.remote_file_size < fstat.st_size:
                for line in self.get_new_lines():
                    yield line

        self.remote_file_size = fstat.st_size
 


    def get_new_lines(self):
        """
        Opens the file and reads any new data from it.
        """

        remote_file = self.sftp_client.open(self.remote_filename, 'r')
        # seek to the latest read point in the file
        remote_file.seek(self.remote_file_size, 0)
        # read any new lines from the file
        line = remote_file.readline()
        while line:
            yield line.strip(self.line_terminators_joined)
            line = remote_file.readline()

        remote_file.close()



    def disconnect(self):
        if self.sftp_client:
            if self.verbose:
                print "Closing SFTP connection..."
            self.sftp_client.close()
            self.sftp_client = None
        if self.client:
            if self.verbose:
                print "Closing SSH connection..."
            self.client.close()
            self.client = None


            

class SSHMultiTailer(object):
    """
    Class to handle tailing of multiple files.
    """

    def __init__(self, host_files, poll_interval=2.0, private_key=None, verbose=False):
        """
        host_files is a dictionary whose keys must correspond to unique
        remote hosts to which this machine has access (ideally via SSH key).
        The values of the host_files dictionary must be arrays of file names
        that must be tailed.
        """

        self.host_files = host_files
        self.poll_interval = poll_interval
        self.private_key = private_key
        self.tailers = {}
        self.verbose = verbose


    def connect(self):
        """
        Connects to all of the host machines.
        """

        if self.verbose:
            print "Connecting to multiple hosts..."

        for host, files in self.host_files.iteritems():
            self.tailers[host] = {}
            for f in files:
                self.tailers[host][f] = SSHTailer(host, f, private_key=self.private_key, verbose=self.verbose)



    def tail(self, report_sleep=False):
        """
        Tails all of the requested files across all of the hosts.
        """

        # make sure we're connected
        if not self.tailers:
            self.connect()

        try:
            # assuming this script is to run until someone kills it (Ctrl+C)
            while 1:
                lines_read = 0

                for host, tailers in self.tailers.iteritems():
                    for filename, tailer in tailers.iteritems():
                        # read as much data as we can from the file
                        for line in tailer.tail():
                            yield host, filename, line
                            lines_read += 1

                if not lines_read:
                    if report_sleep:
                        yield None, None, None
                    self.sleep()

        finally:
            self.disconnect()


    
    def sleep(self):
        time.sleep(self.poll_interval)



    def disconnect(self):
        """
        Disconnects all active connections.
        """

        for host, tailers in self.tailers.iteritems():
            for filename, tailer in tailers.iteritems():
                tailer.disconnect()

        self.tailers = {}

        if self.verbose:
            print "Disconnected from hosts."



