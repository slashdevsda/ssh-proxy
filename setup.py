import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Psychic Bear",
    version = "0.0.5",
    author = "Daimar Anis, Ecuer Thomas, Gelin Guillaume",
    author_email = "ecuer.thomas@gmail.com",
    description = ("SSH interactive session proxy, using paramiko"),
    license = "BSD",
    keywords = "SSH proxy paramiko",
    url = "",
    packages=['psychic_bear'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: Alpha",
        "Topic :: Utilities",
        "License :: BSD License",
    ],
    install_requires=[
        'paramiko',
    ],
    scripts=['scripts/xmlproc_parse', 'scripts/xmlproc_val'],
)      

