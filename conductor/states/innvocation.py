from pypsrp.client import Client
from pypsrp.powershell import PowerShell, RunspacePool
from pypsrp.wsman import WSMan
from pypsrp.shell import WinRS 

from .state import State
from .parseresults import ParseResultsState


class InnvocationState(State):
    """
    The state which indicates the invocation of a command
    """

    __win_client = None
    __win_error_list = []

    def __handle_windows_errors(self, stream):
        if stream.error:
            for item in stream.error:
                return str(item)
                
        if stream.debug:
            for item in stream.debug:
                self.__win_error_list.append(item)
        if stream.information:
            for item in stream.information:
                self.__win_error_list.append(item)
        if stream.verbose:
            for item in stream.verbose:
                self.__win_error_list.append(item)
        if stream.warning:
            for item in stream.warning:
                self.__win_error_list.append(item)
        
    def __create_win_client(self, hostinfo):
        self.__win_client = Client(
            hostinfo.hostname,
            username=hostinfo.username,
            password=hostinfo.password,
            ssl=hostinfo.verify_ssl
        )

    def __invoke_cmd(self, command):
        if not self.__win_client:
            self.__create_win_client(self.hostinfo)
        stdout, stderr, rc = self.__win_client.execute_cmd(command)
        # NOTE: rc (return code of process) should equal 0 but we are not adding logic here this is handled int he ParseResultsState class
        if stderr:
            print('{host} responded with the following message(s): {message}'.format(
                host=self.hostinfo.hostname,
                message=stderr
            ))
        return ParseResultsState(stdout)

    def __invoke_powershell(self, command):
        if not self.__win_client:
            self.__create_win_client(self.hostinfo)
        output, streams, had_errors = self.__win_client.execute_ps(command)
        if had_errors:
            print('{host} responded with the following message(s): {message}'.format(
                host=self.hostinfo.hostname,
                message=self.__handle_windows_errors(streams)
            ))
        return ParseResultsState(output)

    def __invoke_ssh(self,command):
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if hasattr(self.hostinfo, 'ssh_key_path'):
            ssh.connect(
                self.hostinfo.hostname,
                port=self.hostinfo.port,
                username=self.hostinfo.username,
                pkey=self.hostinfo.ssh_key_path
            )
        elif hasattr(self.hostinfo, 'password'):
            ssh.connect(
                self.hostinfo.hostname,
                port=self.hostinfo.port,
                username=self.hostinfo.username,
                password=self.hostinfo.password
            )
        else:
            raise AttributeError('Please provide either a ssh_key_path or a password')
        out = None
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        out = ssh_stdout.read()
        ssh_stdin.flush()
        ssh.close()
        return ParseResultsState(out)

    def invoke(self, hostinfo, command_type, command):
        self.hostinfo = hostinfo
        if command_type == 'powershell':
            result = self.__invoke_powershell(command)
        elif command_type == 'cmd':
            result = self.__invoke_cmd(command)
        elif command_type == 'ssh':
            result = self.__invoke_ssh(command)
        return result