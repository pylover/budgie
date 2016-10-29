import os
import re
from setuptools import setup, find_packages


# reading the package version without loading the package.
with open(os.path.join(os.path.dirname(__file__), 'budgie', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


dependencies = [
    'sqlalchemy',
    'pymlconf',
    'paramiko',
]


setup(
    name="budgie",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    url="https://github.com/pylover/budgie",
    description="A simple workstation observer across intranet.",
    maintainer="Vahid Mardani",
    maintainer_email="vahid.mardani@gmail.com",
    packages=find_packages(),
    install_requires=dependencies,
    license='WTFPL',
    entry_points={
        'console_scripts': [
            'budgie = budgie:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.5',
        # TODO: update classifiers
    ],
)
