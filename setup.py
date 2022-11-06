#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
  name="routetools-cli",
  version="1.0.0",
  description="Tools for route files -- Convert, Add POI, Remove POI",
  author="ysait0",
  url="https://github.com/ysait0/routetools-cli",
  license='MIT',
  packages=["routetools"],
  package_dir={"": "src"},
  scripts=["bin/routetools-cli", "bin/routetools"],
  install_requires=open('requirements.txt', 'r').read().splitlines(),
  classifiers=['License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3',
               'Topic :: Utilities'
               ]
)
