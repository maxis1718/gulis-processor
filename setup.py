#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='gulis',
    version='0.1.0',
    description='maximizes your productivity',
    author='',
    url='https://github.com/maxis1718/gulis',
    download_url='https://github.com/maxis1718/gulis',
    author_email='',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'lxml',
        'requests'
    ]
)
