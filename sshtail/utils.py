import os
import paramiko


def prepend_home_dir(filename):
    """
    Prepends the home directory to the given filename if it doesn't
    already contain some kind of directory path.
    """
    return os.path.join(os.environ['HOME'], '.ssh', filename) if '/' not in filename else filename



def load_rsa_key(filename):
    """
    Function to get an RSA key from the specified file for Paramiko.
    """ 

    return paramiko.RSAKey.from_private_key_file(prepend_home_dir(filename))



def load_dss_key(filename):
    """
    Function to get a DSS key from the specified file for Paramiko.
    """

    return paramiko.DSSKey.from_private_key_file(prepend_home_dir(filename))
