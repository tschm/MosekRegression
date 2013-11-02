MosekRegression
---------------

We created this package to support the experiments given in the paper by Schmelzer, Hauser, Dahl and Andersen. 
Here's a link to the paper http://arxiv.org/abs/1310.3397


Mosek
-----

You need to install Mosek before you can rerun those experiments or create your own ones. We refer to
http://mosek.com/resources/download/

Mosek is commercial software but you can evaluate the product using a 30-day license.

Mosek 7 comes with a new interface called Mosek Fusion. We make heavy use of this interface and solve problems
arising in quantitative finance.

Installation
------------

We provide a setup.py and requirements.txt.

To install this package type python setup.py install.

For more details on this topic see http://docs.python.org/2/install/index.html


Tests
-----
We have created some basic tests. They are available by running nosetests.

Documentation
-------------
Please run makedoc.py to generate the documentation for this product.


IPython Notebooks
-----------------
We also support this package with ipython notebooks. So please try on your bash:

ipython notebook --pylab inline

This should open the notebook and give you access to the notebooks (*.ipynb files).


