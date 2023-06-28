from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='GetHamQuestions',
    url='https://github.com/projectnotions/gethamquestions.git',
    author='K.W.Boyd',
    author_email='kennyb@projectnotions.com',
    # Needed to actually package something
    packages=['gethamquestions'],
    # Needed for dependencies
    install_requires=['re', 'json', 'sys', 'datetime'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='GPLv3',
    description=('Get Amateur Radio Element Questions in a JSON object '
                 'from the official FCC question pools'),
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
import re
import json
import sys
import datetime