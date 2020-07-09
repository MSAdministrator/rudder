from rudder import Rudder, HostInfo

windows_host = '10.0.0.0'
windows_username = 'Administrator'
windows_pass = 'somepassword'

nix_host = '10.0.0.0'
nix_username = 'root'
nix_pass = 'somepassword'

 
hostinfo = HostInfo().windows(
    windows_host,
    windows_username,
    windows_pass
)

conductor = Rudder().execute(hostinfo, 'powershell', 'Get-ChildItem -Path "C:\" -Recurse')
print(conductor)
conductor = Rudder().execute(hostinfo, 'cmd', 'asdf')
print(conductor)


hostinfo = HostInfo().linux(
    nix_host,
    nix_username,
    password=nix_pass
)
conductor = Rudder().execute(hostinfo, 'ssh', 'ls -al')
print(conductor)
