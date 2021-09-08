import typing
import attr

from .core import Core


@attr.s
class Host:

    hostname = attr.ib(type=str)
    username = attr.ib(default=None, type=str)
    password = attr.ib(default=None, type=str)
    verify_ssl = attr.ib(default=False, type=bool)
    ssh_key_path = attr.ib(default=None, type=str)
    port = attr.ib(default=22, type=int)
    timeout = attr.ib(default=5, type=int)

    @ssh_key_path.validator
    def validate_ssh_key_path(self, attribute, value):
        if value:
            Core.get_abs_path(value)


@attr.s
class Runner:

    executor = attr.ib(type=str)
    command = attr.ib(type=str)
    hosts: typing.List[Host] = attr.ib()

    @executor.validator
    def validate_type(self, attribute, value):
        if value not in ['powershell', 'cmd', 'ssh']:
            raise ValueError("Please provide a value for type of either 'powershell','cmd', or 'ssh'")
