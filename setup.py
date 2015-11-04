# -*- coding: utf-8 -*-

import os
import sys

__DIR__ = os.path.abspath(os.path.dirname(__file__))

import codecs
from setuptools import setup
from setuptools.command.test import test as TestCommand
import shissen


def read(filename):
    """Read and return `filename` in root dir of project and return string"""
    return codecs.open(os.path.join(__DIR__, filename), 'r').read()


install_requires = read("requirements.txt").split()
long_description = read('README.md')


class Pytest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--verbose']
        self.test_suite = True

    def run_tests(self):
        # Using pytest rather than tox because Travis-CI has issues with tox
        # Import here, cause outside the eggs aren't loaded
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name="shissen",
    version=shissen.__version__,
    url='https://github.com/vltr/shissen',
    license='MIT License',
    author='Richard Kuesters',
    description=('A simple JSON API framework based on Cyclone'),
    long_description=long_description,
    packages=['shissen'],
    install_requires=install_requires,
    tests_require=['pytest'],
    cmdclass={'test': Pytest},
    data_files=[
        # Populate this with any files config files etc.
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ]
)
