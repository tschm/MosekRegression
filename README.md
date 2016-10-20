# MosekTools
#### Building tools on the shoulders of [Mosek](http://www.mosek.com).


## Motivation

We created this package to support the experiments given in the [paper](http://arxiv.org/abs/1310.3397) 
by Schmelzer, Hauser, Dahl and Andersen. 


## Installation

We provide a build.sh file that creates a local environment using the popular (mini)conda package. 
Using this approach we install Mosek on the fly (via pip).
Mosek is commercial software but you can evaluate the product using a 30-day license.

Mosek 8 comes with a new interface called Mosek Fusion. We make heavy use of this interface and solve common problems
arising in quantitative finance.

## License

To use Mosek you need to install a Mosek license. An easy way to achieve that is to dump a file called mosek.lic in the folder license.

## Applications

You can solve various (un)constrained regression and Markowitz problems.








