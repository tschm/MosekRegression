# MosekTools
#### Building tools on the shoulders of [Mosek](http://www.mosek.com).


## Motivation

We created this package to support the experiments given in the [paper](http://arxiv.org/abs/1310.3397) 
by Schmelzer, Hauser, Dahl and Andersen. 


## Mosek

You need to [install Mosek](http://mosek.com/resources/download/) before you can use this package.
Mosek is commercial software but you can evaluate the product using a 30-day license.

Mosek 7 comes with a new interface called Mosek Fusion. We make heavy use of this interface and solve common problems
arising in quantitative finance.

## Installation

To install this package type at your bash or command line 

```
python setup.py install. 
```

For more details see [here](http://docs.python.org/2/install/index.html)


## Tests
We have created some basic tests. Execute on your bash or command line

```
nosetests
```

## Documentation
Run 
```
python makedoc.py
```
to generate the documentation for this product.


## Applications

* [**Data**](http://nbviewer.ipython.org/urls/raw.github.com/tschm/MosekRegression/master/Data.ipynb)
   
   We have created a small tool based on pandas and yahoo finance to extract financial time series data. 
   Fetching data from the web is slow and hence we recommend to store the data locally and reuse it for experiments.

* [**Equity Portfolios**] (http://nbviewer.ipython.org/urls/raw.github.com/tschm/MosekRegression/master/EquityPortfolios.ipynb)

   Common equity portfolios

