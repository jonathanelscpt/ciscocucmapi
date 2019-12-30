#!/usr/bin/env python

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name="ciscocucmapi",
    version='0.0.1',
    license="MIT",
    description="Python Wrappers for Cisco CUCM SOAP APIs",
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Jonathan Els',
    author_email='jonathanelscpt@gmail.com',
    url='https://github.com/jonathanelscpt/ciscocucmapi',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Communications :: Telephony',
        'Topic :: Communications :: Conferencing',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://ciscocucmapi.readthedocs.io/',
        'Changelog': 'https://ciscocucmapi.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/jonathanelscpt/ciscocucmapi/issues',
    },
    keywords=[
        "cisco", "cucm", "uc", "collaboration", "callmanager", "axl",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.18.4',
        'zeep>=2.5.0'
    ],
    extras_require={
        'rst': ['docutils>=0.11'],
        # ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'ciscocucmapi = ciscocucmapi.cli:main',
        ]
    },
)
