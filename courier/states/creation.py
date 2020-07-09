from .state import State
from .innvocation import InnvocationState


class CreationState(State):
    """
    The state which is used to modify commands provided to rudder
    """

    def powershell(self, event):
        command = None
        if event:
            if '\n' in event or '\r' in event:
                if '\n' in event:
                    command = event.replace('\n', '; ')
                if '\r' in event:
                    if command:
                        command = command.replace('\r', '; ')
                    else:
                        command = event.replace('\r', '; ')
            return InnvocationState()

    def cmd(self):
        return InnvocationState()

    def ssh(self):
        return InnvocationState()

    def on_event(self, command_type, command):
        if command_type == 'powershell':
            return self.powershell(command)
        elif command_type == 'cmd':
            return self.cmd()
        elif command_type == 'ssh':
            return self.ssh()
        return self