from .core import Core
from .runner import Runner, Host
from .states.creation import CreationState


class Rudder(Core):
    """ 
    A simple state machine that runs commands remotely on the targeted system

        ## Create Host Object and running a command
            from rudder import Host

            my_host_list = []
            my_host_list.append(
                Host(
                    hostname='10.10.32.100',
                    username='admin',
                    password='secret_password1'
                )
            )

            rudder = Rudder(hosts=my_host_list)
            for result in rudder.execute(executor='powershell', command='Get-ChildItem -Path "C:\" -Recurse'):
                print(result)

        ## Providing a config_file_path
            from rudder import Rudder

            rudder = Rudder(config_file_path='~/path_to_config_file.yml')
            for result in rudder.execute():
                print(result)
    """

    def execute(self, 
        host: Host = [None],
        config_file_path: str  = None,
        executor: str = None, 
        command: str = None):
        """The execute method is the main entry point to execute the provided command on a remote host.

        You must create a host object and pass it to this method along with the executor and command to execute.

        Args:
            host (Host, optional): Create a list of one or more Host objects and provide this as input. Defaults to [None].
            config_file_path (str, optional): A path to a local config file. Defaults to None.
            executor (str, optional): A executor of powershell or cmd or ssh is needed. 
                                      Default is None but must be provided if not using a config_file_path
            command (str, optional): The command to run on a specified remote host
                                     Default is None but must be provided if not using a config_file_path

        Returns:
            str: Returns the results from a remote command
        """
        if host:
            self.__host_info = host
        else:
            self.__host_info = None
        if config_file_path:
            self.__configs = self.parse_config_file(config_file_path)
        else:
            self.__configs = None
        self.__logger.debug('Intializing default state of CreationState')
        self.state = CreationState()
        if not self.__configs and self.__host_info and executor in ['powershell', 'cmd', 'ssh'] and command:
            self.__configs = [Runner(
                executor=executor,
                command=command,
                hosts=self.__host_info
            )]
        elif self.__configs:
            pass
        else:
            raise ValueError('You must provide a valid executor and command or a properly formatted config file')
        if self.__configs:
            for config in self.__configs:
                for host in config.hosts:
                    finished = False
                    while not finished:
                        if str(self.state) == 'CreationState':
                            self.__logger.debug('Running CreationState on_event')
                            self.state = self.state.on_event(config.executor, config.command)
                        if str(self.state) == 'InnvocationState':
                            self.__logger.debug('Running InnvocationState on_event')
                            self.state = self.state.invoke(host, config.executor, config.command)
                        if str(self.state) == 'ParseResultsState':
                            self.__logger.debug('Running ParseResultsState on_event')
                            yield self.state.on_event()
                            finished = True
