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


http://nbviewer.ipython.org/urls/raw.github.com/tschm/MosekRegression/master/Minimum%20Variance.ipynb
http://nbviewer.ipython.org/urls/raw.github.com/tschm/MosekRegression/master/Data.ipynb

Further Topics
--------------
Some links for next steps:

* http://stackoverflow.com/questions/5246843/how-to-get-a-complete-list-of-ticker-symbols-from-yahoo-finance
* http://blog.miguelgrinberg.com/post/the-package-dependency-blues
* http://stackoverflow.com/questions/15422527/best-practices-how-do-you-list-required-dependencies-in-your-setup-py
* http://penandpants.com/2013/04/25/data-provenance-with-gitpython/

