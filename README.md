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

Whether you are wanting to run a command remotely on Windows or a *nix based system (e.g. CentOS, macOS, etc.) you first need to create a `HostInfo` object.  You do this by importing the `HostInfo` class in your script like so:

```python
from rudder import HostInfo
```

### Windows HostInfo Object

You first need to provide the following information when instantiating a `HostInfo` object for Windows systems:

```python
from rudder import HostInfo

windows_host = '10.0.0.0'
windows_username = 'Administrator'
windows_pass = 'somepassword'
 
hostinfo = HostInfo().windows(
    windows_host,
    windows_username,
    windows_pass
)
```

### *Nix HostInfo Object

You first need to provide the following information when instantiating a `HostInfo` object for *nix systems:

```python
from rudder import HostInfo

nix_host = '10.0.0.0'
nix_username = 'root'
nix_pass = 'somepassword'
# Optionally you can provide the following parameters:
# ssh_key_path = '/Users/username/.ssh/id_rsa'
# port = '2222'
 
hostinfo = HostInfo().linux(
    nix_host,
    nix_username,
    password=nix_pass
    ssh_key_path=None,
    port=22
)
```

### Running Command Remotely on Windows

With rudder you can run either `cmd` or `powershell` commands remotely.  Below are two examples of these methods:

```python
from rudder import Rudder, HostInfo

windows_host = '10.0.0.0'
windows_username = 'Administrator'
windows_pass = 'somepassword'
 
hostinfo = HostInfo().windows(
    windows_host,
    windows_username,
    windows_pass
)

conductor = Rudder().execute(hostinfo, 'powershell', 'Get-ChildItem -Path "C:\" -Recurse')
print(conductor)
conductor = Rudder().execute(hostinfo, 'cmd', 'dir')
print(conductor)
```

### Running Command Remotely on *Nix

With rudder you can run commands remotely using SSH and whichever shell is avaialble on the remote system:

```python
from rudder import Rudder, HostInfo

nix_host = '10.0.0.0'
nix_username = 'root'
nix_pass = 'somepassword'
 
hostinfo = HostInfo().linux(
    nix_host,
    nix_username,
    password=nix_pass
)
conductor = Rudder().execute(hostinfo, 'ssh', 'ls -al')
print(conductor)
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