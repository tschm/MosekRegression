from setuptools import setup, find_packages

setup(
    name='MosekRegression',
    version='1.3',
    packages=find_packages(include='mosekTools*'),
    url='https://github.com/tschm/MosekRegression',
    license='',
    author='Thomas Schmelzer, Joachim Dahl',
    author_email='thomas.schmelzer@gmail.com',
    description='Experiments & Tools for the new Mosek Fusion interface'
)
