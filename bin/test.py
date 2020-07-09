from conductor import Conductor, HostInfo

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

conductor = Conductor().execute(hostinfo, 'powershell', 'Get-ChildItem -Path "C:\" -Recurse')
print(conductor)
conductor = Conductor().execute(hostinfo, 'cmd', 'asdf')
print(conductor)


hostinfo = HostInfo().linux(
    nix_host,
    nix_username,
    password=nix_pass
)
conductor = Conductor().execute(hostinfo, 'ssh', 'ls -al')
print(conductor)
