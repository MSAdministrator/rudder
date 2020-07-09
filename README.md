# conductor

`conductor` is a Python package to run commands remotely on Windows, macOS or *nix systems using PowerShell Remoting/WinRM or SSH.

## Getting Started

In order to use conductor you must make sure you have access and credentials to authenticate to a remote host.

### Prerequisites

The following packages will be installed and are prerequisities for conductor:

```
paramiko
fire
pypsrp
```

### Installing

Install this package using `pip`:

```bash
pip3 install conductor
```

Or you can clone this repository and install locally:

```bash
git clone https://github.com/MSAdministrator/conductor.git
cd conductor
python3 setup.py install
```

## Built With

* [carcass](https://github.com/MSAdministrator/carcass) - Python packaging template

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* MSAdministrator - *Initial work* - [MSAdministrator](https://github.com/MSAdministrator)

See also the list of [contributors](https://github.com/MSAdministrator/conductor/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details