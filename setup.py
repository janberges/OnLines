#!/usr/bin/env python3

import setuptools

with open('README.md', 'r', encoding='utf-8') as README:
    long_description = README.read()

setuptools.setup(
    name                          = 'OnLines',
    version                       = '2021.1',
    author                        = 'Jan Berges',
    author_email                  = '',
    description                   = 'Line plots with Python and SVG',
    long_description              = long_description,
    long_description_content_type = 'text/markdown',
    url                           = 'https://bitbucket.org/berges/OnLines',
    py_modules                    = ['onlines'],
    python_requires               = '>=2.7',
    install_requires              = [],
    classifiers                   = [
        'Programming Language :: Python',
        'License :: Freely Distributable',
        'Operating System :: POSIX :: Linux',
        ],
    )
