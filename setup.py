# -*- coding: utf-8 -*-
"""
    comic
    ~~~~~

    A simple, fast, and fun web comic static site generator.
"""


from setuptools import find_packages, setup


setup(

    # Basic package information:
    name = 'comic',
    version = '0.0.1',
    entry_points = {
        'console_scripts': [
            'comic = comic.cli:main'
        ],
    },
    packages = find_packages(),

    # Packaging options:
    zip_safe = False,
    include_package_data = True,

    # Package dependencies:
    install_requires = [
        'Jinja2==2.7.3',
        'PyYAML==3.11',
        'docopt==0.6.2',
    ],

    # Metadata for PyPI:
    author = 'Randall Degges',
    author_email = 'r@rdegges.com',
    license = 'UNLICENSE',
    url = 'https://github.com/rdegges/comic',
    keywords = ['comic', 'generator', 'static', 'webcomic'],
    description = 'A simple, fast, and fun web comic static site generator.',
    long_description = __doc__,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],

)
