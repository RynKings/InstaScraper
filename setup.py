# -*- coding: utf-8 -*-

from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

import InstaScraper

setup(
    name='InstaScraper',
    packages=['InstaScraper'],
    version=InstaScraper.__version__,
    license='GNU General Public License v3 (GPLv3)',
    author=InstaScraper.__author__,
    author_email=InstaScraper.__author_email__,
    url=InstaScraper.__url__,
    description='Instagram Scraper',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'requests'
        'pickle'
    ],
)