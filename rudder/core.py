import os
import yaml

from .utils.logger import LoggingBase


class Core(metaclass=LoggingBase):

    def get_abs_path(self, value):
        """Formats and returns the absolute path for a path value

        Args:
            value (str): A path string in many different accepted formats

        Returns:
            str: The absolute path of the provided string
        """
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    def parse_config_file(self, config_file_path):
        config = None
        return_list = []
        try:
            with open(self.get_abs_path(config_file_path), 'r', encoding="utf-8") as f:
                config = yaml.load(f.read(), Loader=yaml.SafeLoader)
        except:
            # windows does not like get_abs_path so casting to string
            with open(str(config_file_path), 'r', encoding="utf-8") as f:
                config = yaml.load(f.read(), Loader=yaml.SafeLoader)
        if config and config.get('inventory') and config.get('run_conditions'):
            from .runner import Runner, Host
            for key,val in config['run_conditions'].items():
                for inventory in val['inventories']:
                    if config['inventory'].get(inventory):
                        host_list = []
                        inputs = config['inventory'][inventory]['inputs']
                        for host in config['inventory'][inventory]['hosts']:
                            host_list.append(
                                Host(
                                    hostname=host,
                                    username=inputs.get('username'),
                                    password=inputs.get('password'),
                                    verify_ssl=inputs['verify_ssl'] if inputs.get('verify_ssl') else False,
                                    ssh_key_path=inputs.get('ssh_key_path'),
                                    port=inputs['port'] if inputs.get('port') else 22,
                                    timeout=inputs['timeout'] if inputs.get('timeout') else 5
                                )
                            )
                        if host_list:
                            return_list.append(
                                Runner(
                                    executor=val['executor'],
                                    command=val['command'],
                                    hosts=host_list
                                )
                            )
        return return_list
