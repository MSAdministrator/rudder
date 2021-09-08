# rudder

`rudder` is a Python package to run commands remotely on Windows, macOS or *nix systems using PowerShell Remoting/WinRM or SSH.

## Getting Started

In order to use rudder you must make sure you have access and credentials to authenticate to a remote host.

### Prerequisites

The following packages will be installed and are prerequisities for rudder:

```
paramiko
fire
pypsrp
```

> NOTE: To use this on your remote Windows machines, you need to do the following:

1. Run from an elevated PowerShell prompt

```powershell
winrm quickconfig (type yes)
Enable-PSRemoting (type yes)
# Set start mode to automatic
Set-Service WinRM -StartMode Automatic
# Verify start mode and state - it should be running
Get-WmiObject -Class win32_service | Where-Object {$_.name -like "WinRM"}
```

2. Additionally you may need to specify the allowed host to remote into systems:

```powershell
# Trust hosts
Set-Item 'WSMan:localhost\client\trustedhosts' -value * -Force 
NOTE: don't use the * for the value parameter in production - specify your Swimlane instance IP
# Verify trusted hosts configuration
Get-Item WSMan:\localhost\Client\TrustedHosts
```

3. Additional Troubleshooting

```powershell
#If you receive a timeout error or something like that, check and make sure that your remote Windows host network is set to Private and NOT public. You can change it using the following:

# Get Network Profile
Get-NetConnectionProfile

# if the NetworkCategory is set to Public then run the following to set it to Private

Set-NetConnectionProfile -InterfaceAlias Ethernet0 -NetworkCategory Private
# try it again
```

### Installing

Install this package using `pip`:

```bash
pip3 install rudder
```

Or you can clone this repository and install locally:

```bash
git clone https://github.com/MSAdministrator/rudder.git
cd rudder
python3 setup.py install
```

## Usage

Below contains two prime examples of using rudder on both Windows and a *nix system.

Whether you are wanting to run a command remotely on Windows or a *nix based system (e.g. CentOS, macOS, etc.) you first need to create a `Host` object.  You do this by importing the `Host` class in your script like so. Once imported you can provide a list of one or more `Host` objects to rudder (more info below):

```python
from rudder import Host

my_host_list = []
my_host_list.append(
    Host(
        hostname=None, # nix & windows
        username=None, # nix & windows
        password=None, # nix & windows
        verify_ssl=False, # windows
        ssh_key_path=None, # nix
        port=22, # nix
        timeout=5, # nix
    )
)
```

### Running Command Remotely Using Username & Password

With rudder you can run either `ssh`, `cmd` or `powershell` commands remotely.  Below are examples of these methods:

```python
from rudder import Rudder, Host

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

```

### Running Command Remotely using SSH key

With rudder you can run commands remotely using SSH and whichever shell is avaialble on the remote system:

```python
from rudder import Rudder, Host

my_host_list = []
# If no ssh_key_path or no username and password, Rudder
# will attempt to use the default path for these keys
my_host_list.append(
    Host(
        hostname='10.10.32.100'
    )
)

my_host_list.append(
    Host(
        hostname='10.32.1.1',
        ssh_key_path='~/some_path
    )
)

rudder = Rudder(hosts=my_host_list)
for result in rudder.execute(executor='ssh', command='ls -al'):
    print(result)

```


### Running Command Remotely using Config File

With rudder you can provide a formatted config file to automate rudder even further. Below is an example of the format of this configuration file:

```yaml
inventory: # Inventory contains one or more groups of hosts and how you can authenticate to them
  windows1: # <- This can be any name but make it clear to you
    inputs: # <- How I am going to authenticate to these hosts
      username: some_username
      password: secret_password
      verify_ssl: false
    hosts: # <- A list of one or more hosts that work with the provided inputs above
      - 192.168.1.1
      - 10.32.1.1
      # Add as many as needed
  linux1:
    inputs: # <- How I am going to authenticate to these hosts
      username: some_username
      password: secret_password
      ssk_key_path: path_to_a_ssh_private_key
      port: 22
      timeout: 5
    hosts: # <- A list of one or more hosts that work with the provided inputs above
      - 10.32.100.201
      - 10.32.0.1
      # Add as many as needed

run_conditions:
  some_group_name: # <- A grouping of one or more inventories (hosts)
    executor: ssh # <- The executor to use. Options are ssh, cmd, powershell.
    inventories: # <- One or more inventory defintions from above
      - linux1
    command: | # <- The command to run on all the inventory defintions above
      ls -al
  my_windows_group_name:
    executor: powershell # or cmd
    inventories:
      - windows1
    command: |
      Get-ChildItem
```

By providing a path to this configuration file to rudder will parse the config file and ensure it's in it's expected format.

After you have instantiated a `Rudder` object then all you need to do is call the `execute` method with no additional paramter values.

```python
from rudder import Rudder

rudder = Rudder(config_file_path='~/path_to_config_file.yml')
for result in rudder.execute():
    print(result)
```

## Built With

* [carcass](https://github.com/MSAdministrator/carcass) - Python packaging template

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* MSAdministrator - *Initial work* - [MSAdministrator](https://github.com/MSAdministrator)

See also the list of [contributors](https://github.com/MSAdministrator/rudder/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details