import sys


class HostInfo(object):

    """A HostInfo object is used when executing remote commands on hosts
    """

    def windows(self, hostname, username, password, verify_ssl=False):
        """The windows method provides information to connect to a remote windows host using the PowerShell Remoting Protocol and WinRM

        Args:
            hostname (str): A single hostname to connect to.  Either DNS or IP address.
            username (str): A username that has access to remote into this machine
            password (str): A password that works with the username provided
            verify_ssl (bool, optional): Whether or not you are using TLS/SSL certificates. Defaults to False.

        Returns:
            HostInfo: Returns a HostInfo object used to connect to a remote Windows host
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        return self

    def linux(self, hostname, username, ssh_key_path=None, password=None, port=22):
        """The linux method provides information to execute code on a remote host using SSH.  This can be Linux or macOS.

        Args:
            hostname (str): A single hostname to connect to.  Either DNS or IP address.
            username (str): A username that has access to remote into this machine
            password (str, optional): A password that works with the username provided.
            ssh_key_path (str, optional): A ssh key path to authenticate to a remote host
            port (int, optional): The port to use when SSHing. Defaults to 22.

        Returns:
            HostInfo: Returns a HostInfo object used to connect to a remote Linux or macOS host
        """
        self.hostname = hostname
        self.username = username
        
        if ssh_key_path:
            self.ssh_key_path = ssh_key_path
        elif password:
            self.password = password
        else:
            raise AttributeError('Please provide a ssh key path or a password!')
        self.port = port
        return self
