import os

import yaml
from git import InvalidGitRepositoryError, Repo
from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

# parse_requirements() returns a generator of pip.req.InstallRequirement objects
install_requirements = parse_requirements('requirements.txt', session='hack')

# requirements is a list of requirement
requirements = [str(ir.requirement) for ir in install_requirements]


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

project_name = 'otp'

try:
    repo = Repo('.')
    urls = list(repo.remotes['origin'].urls)
    project_url = urls[0]
except InvalidGitRepositoryError:
    project_url = ''

setup(
    author='Pietro Atzeni',
    author_email='pietrino.atzeni@gmail.com',
    name=project_name,
    url=project_url,
    version=read('version'),
    description=project_name,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=(find_packages(exclude=["docs", "tests", "tests.*"])),
    platforms=['any'],
    entry_points={
        'console_scripts': [
            '{0} = {1}.cli.main:main'.format(project_name, project_name.replace('-', '_'))
        ]
    },
    test_suite='tests',
    install_requires=requirements,
    include_package_data=True,
)
