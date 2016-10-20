#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='MosekRegression',
    version="v1.3",
    packages=find_packages(include='books/mosekTools*'),
    url='https://github.com/tschm/MosekRegression',
    license='',
    author='Thomas Schmelzer, Joachim Dahl',
    author_email='thomas.schmelzer@gmail.com',
    description='Experiments & Tools for the new Mosek Fusion interface',
    install_requires=['pandas>=0.18.0', 'Mosek>=8.0']
)
