import wonk

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as req_file:
    requirements = req_file.read().split('\n')

with open('dev-requirements.txt') as devreq_file:
    test_requirements = devreq_file.read().split('\n')


setup(
    name = 'wonk',
    author = "Patrik Beyls",
    url = 'https://github.com/beylsp/wonk-server',
    packages = [
        'wonk',
    ],
    install_requires = requirements,
    license = "MIT",
    test_suite = 'tests',
    tests_require = test_requirements,
)
