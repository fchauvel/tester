#!/usr/bin/env python


from setuptools import setup

from tester import __program__, __version__, __description__, __maintainer__, __email__, __command__


setup(name=__program__,
      version=__version__,
      description=__description__,
      author=__maintainer__,
      author_email=__email__,
      url="https://github.com/fchauvel/tester",
      packages=["tester"],
      test_suite="tests",
      entry_points = {
          'console_scripts': [
              __command__ + " = tester.start:main"
          ]
      }
     )
