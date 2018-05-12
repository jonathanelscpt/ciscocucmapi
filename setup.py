# -*- coding: utf-8 -*-
"""setuptools based setup module."""

import io
from os.path import splitext
from os.path import basename
from os.path import dirname
from os.path import join
from glob import glob
from setuptools import setup, find_packages


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


install_requires = [
    'requests>=2.18.4',
    'urllib3>=1.22',
    'zeep>=2.5.0',
    'lxml>=4.2.1'
]
# tests_require = [
#     'pytest-httpbin==0.0.7',
#     'pytest-cov',
#     'pytest-mock',
#     'pytest-xdist',
#     'PySocks>=1.5.6, !=1.5.7',
#     'pytest>=2.8.0'
# ]


setup(
    name="UCToolkit",
    version="0.0.1",
    license="MIT",
    description="Python Toolkit for Cisco UC APIs",
    long_description=read('README.md'),
    author="Jonathan Els",
    author_email="jonathanelscpt@gmail.com",
    url="https://github.com/jonathanelscpt/UCToolkit",
    python_requires=">=3.6.*",
    packages=find_packages('src'),
    package_dir={
        '': 'src'
    },
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
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
    ],
    keywords=[
        "cisco", "cucm", "uc", "collaboration", "callmanager", "axl",
    ],
    install_requires=install_requires,
    # tests_require=tests_require,
    extras_require={},
    entry_points={},
)

