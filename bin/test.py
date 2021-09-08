from rudder import Rudder, HostInfo, Host, runner

password = 'UR4Swimlane!'


def capture(f):
    """
    Decorator to capture standard output
    """
    def captured(*args, **kwargs):
        import sys
        from io import StringIO

        # setup the environment
        backup = sys.stdout

        try:
            sys.stdout = StringIO()     # capture output
            f(*args, **kwargs)
            out = sys.stdout.getvalue() # release output
        finally:
            sys.stdout.close()  # close the stream 
            sys.stdout = backup # restore original stdout

        return out # captured output wrapped in a string

    return captured



windows_host = '10.32.0.250'
windows_username = 'Administrator'


nix_host = '10.32.100.201'
nix_username = 'root'


'''
hostinfo = HostInfo().windows(
    windows_host,
    windows_username,
    password=password
)

response = Rudder().execute(hostinfo, 'powershell', "Get-ChildItem -Recursive")
print(response)
input('press')
conductor = Rudder().execute(hostinfo, 'cmd', 'dir')
print(conductor)


'''

#hostinfo = HostInfo(config_file_path='./config.yml').linux(
#    nix_host,
#    nix_username,
#    password=password
#)
#print(hostinfo)
my_list = []
my_list.append(
    Host(
        hostname=nix_host,
        username=nix_username,
        password=password
    )
)
rudder = Rudder(host=my_list)# config_file_path='./config.yml')
for item in rudder.execute(executor='ssh', command='ls -al'):
    print(item)
#print(rudder.execute())
#conductor = Rudder().execute(hostinfo, 'ssh', 'ip addr')
#print(conductor)