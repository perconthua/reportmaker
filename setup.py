# -*- coding: utf-8 -*-

import os
import re
import time
from setuptools import setup, find_packages

def read_file(filename):
    with open(filename, 'r') as infile:
        return infile.read()

requires = [
    "falcon==0.2.0b1",
    "Cython==0.21.1",
    "colander==1.0",
    "mongoengine==0.8.7",
    "gunicorn==18.0"
]

extras_require = {
    "test": [
        "nose",
        "coverage",
        "flake8",
        "mock"
    ]
}


setup(name=name_project,
        version='0.1.0',
        description='Really Fast API',
        long_description=read_file('README.md'),
        author='Percy Contreras',
        author_email='pontreras@rcp.pe',
        keywords='web wsgi falcon restful reportmaker api',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        test_suite='gateway',
        install_requires=requires,
        extras_require=extras_require,
    )
    