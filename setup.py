from setuptools import setup
from setuptools import find_packages

setup(
    name='python-zilore',
    version='0.0.2',
    description="Zilore DNS API Wrapper",
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
