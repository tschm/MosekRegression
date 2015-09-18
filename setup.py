import sys
import os
from setuptools import setup, find_packages

version = "v1.1"

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

setup(
    name='MosekRegression',
    version=version[1:],
    packages=find_packages(include='mosekTools*'),
    url='https://github.com/tschm/MosekRegression',
    license='',
    author='Thomas Schmelzer, Joachim Dahl',
    author_email='thomas.schmelzer@gmail.com',
    description='Experiments & Tools for the new Mosek Fusion interface',
    install_requires=['pandas>=0.16.2', 'Mosek>=7.1']
)
