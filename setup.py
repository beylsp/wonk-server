try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as req_file:
    requirements = req_file.read().split('\n')


setup(
    name = 'wonk',
    author = "Patrik Beyls",
    url = 'https://github.com/beylsp/wonk-server',
    packages = [
        'wonk',
    ],
    install_requires = requirements,
    license = "MIT",
)
