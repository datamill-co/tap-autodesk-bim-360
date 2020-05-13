#!/usr/bin/env python

from setuptools import setup

setup(name='tap-autodesk-bim-360',
      version='0.0.1',
      description='Singer.io tap for extracting data from the Autodesk Forge BIM 360 API',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_autodesk_bim_360'],
      install_requires=[
        'backoff==1.8.0',
        'ratelimit==2.2.1',
        'requests==2.23.0',
        'singer-python==5.9.0'
      ],
      entry_points='''
          [console_scripts]
          tap-autodesk-bim-360=tap_autodesk_bim_360:main
      ''',
      packages=['tap_autodesk_bim_360'],
      package_data = {
          'tap_autodesk_bim_360': ['schemas/*.json'],
      }
)
