#! /usr/bin/env python

from distutils.core import setup

setup(name="escs",
      version="0.0.0",
      description="",
      packages=["cspkg", 
      "cspkg.plugins"],
      scripts=['escs'],
      package_data={'cspkg': ['escsrc']},
      author="Iury O. G. Figueiredo",
      author_email="last.src@gmail.com",
      url='',
      keywords=[],
      classifiers=[])

