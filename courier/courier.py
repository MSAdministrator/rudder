from .states.creation import CreationState


class Courier(object):
    """ 
    A simple state machine that mimics the functionality of a device from a 
    high level.
    """

    def __init__(self):
        """ Initialize the components. """

        # Start with a default state.
        self.state = CreationState()

    def execute(self, hostinfo, command_type: str, command: str):
        """The execute method is the main entry point to execute the provided command on a remote host.

        You must create a host object and pass it to this method along with the command_type and command to execute.

        Args:
            hostinfo (HostInfo): A host information object must be created and passed into this method
            command_type (str): A command_type of powershell or cmd or ssh is needed
            command (str): The command to run on a specified remote host

        Returns:
            str: Returns the results from a remote command
        """        
        while True:
            if str(self.state) == 'CreationState':
                self.state = self.state.on_event(command_type, command)
            if str(self.state) == 'InnvocationState':
                self.state = self.state.invoke(hostinfo, command_type, command)
            if str(self.state) == 'ParseResultsState':
                return self.state.on_event()
