
from setuptools import setup, find_packages

setup(
    name='tdntools',
    packages=find_packages(exclude=['tests*']),  # this must be the same as the name above
    version='0.1.0',
    url='https://github.com/darofar/tdntools',  # use the URL to the github repo
    install_requires=["pyasn1-modules","scrapy"],
    tests_require=['mock','nose','coverage'],
    classifiers=[]
)