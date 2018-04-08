# -*- coding: utf-8 -*-
"""setuptools based setup module."""


import os
from codecs import open
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

packages = ['uctoolkit']

requires = [
    'aiohttp==>=3.1.2',
    'future>=0.16.0',
    'requests>=2.18.4',
    'urllib3>=1.22',
    'zeep>=2.5.0',
]
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
    python_requires=">=3.6.*",
    packages=find_packages(include=['uctoolkit', 'uctoolkit.*']),
    package_dir={'uctoolkit': 'uctoolkit'},
    package_data={
        '': ['LICENSE', 'README.md'],
        'examples': ['*.py']
    },
    include_package_data=True,
    install_requires=requires,
    # tests_require=test_requirements,
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
)
