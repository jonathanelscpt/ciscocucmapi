# -*- coding: utf-8 -*-
"""setuptools based setup module."""


import os
from codecs import open
from setuptools import setup, find_packages
from pip.req import parse_requirements


here = os.path.abspath(os.path.dirname(__file__))

packages = ['uctoolkit']

# requires = [
#     'chardet>=3.0.2,<3.1.0',
#     'idna>=2.5,<2.7',
#     'urllib3>=1.21.1,<1.23',
#     'certifi>=2017.4.17'
#
# ]
# test_requirements = [
#     'pytest-httpbin==0.0.7',
#     'pytest-cov',
#     'pytest-mock',
#     'pytest-xdist',
#     'PySocks>=1.5.6, !=1.5.7',
#     'pytest>=2.8.0'
# ]

about = {}
with open(os.path.join(here, 'uctoolkit', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=find_packages(include=['uctoolkit', 'uctoolkit.*']),
    package_data={
        '': ['LICENSE', 'README.md'],
        'examples': ['*.py']
    },
    package_dir={'uctoolkit': 'uctoolkit'},
    include_package_data=True,
    python_requires=">=3.6.*",
    install_requires=requires,
    license=about['__license__'],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Telephony',
        'Topic :: Communications :: Conferencing',
        'Topic :: System :: Systems Administration'
    ),
    keywords='cisco cucm uc collaboration callmanager axl',
    # cmdclass={'test': PyTest},
    # tests_require=test_requirements,
    # extras_require={
    #     'security': ['pyOpenSSL>=0.14', 'cryptography>=1.3.4', 'idna>=2.0.0'],
    #     'socks': ['PySocks>=1.5.6, !=1.5.7'],
    #     'socks:sys_platform == "win32" and (python_version == "2.7" or python_version == "2.6")': ['win_inet_pton'],
    # },
)
