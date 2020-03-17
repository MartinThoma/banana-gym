#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Third party
from setuptools import find_packages, setup

setup(
    name="gym_banana",
    version="0.0.2",
    install_requires=["gym>=0.2.3", "pandas", "cfg_load"],
    packages=find_packages(),
)
