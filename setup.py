from setuptools import setup
from setuptools import find_packages

from codecs import open
from os import path, listdir

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-zilore',
    version='0.0.4',
    description="Zilore DNS API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="clyang",
    author_email='clyang@clyang.net',
    url='https://github.com/clyang/python-zilore',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=['ziloreapi'],
    install_requires=['requests']
)
