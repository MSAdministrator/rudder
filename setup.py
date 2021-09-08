from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

version = dict()
with open("./rudder/utils/version.py") as fp:
    exec(fp.read(), version)


setup(
    name='rudder',
    version=version['__version__'],
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package to execute code remotely to multiple operating system platforms',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=required,
    keywords=['rudder', 'winrm', 'ssh', 'cmd', 'powershell'],
    url='https://github.com/MSAdministrator/rudder',
    author='MSAdministrator',
    author_email='rickardja@live.com',
    python_requires='>3.6',
    package_data={
        'rudder':  ['data/logging.yml']
    },
    entry_points={
          'console_scripts': [
              'rudder = rudder.__main__:main'
          ]
    }
)