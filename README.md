# MosekTools
#### Building tools on the shoulders of [Mosek](http://www.mosek.com).


## Motivation

We created this package to support the experiments given in the [paper](http://arxiv.org/abs/1310.3397) 
by Schmelzer, Hauser, Dahl and Andersen. 


## Installation

A first glimpse of the notebooks we provide is given here:
http://nbviewer.jupyter.org/github/tschm/MosekRegression/tree/master/books/

For reproducing our results in exactly the environment we have used clone the underlying repository

    git clone git@github.com:tschm/MosekRegression.git

and build the pymosek docker container with

    docker-compose build pymosek
    
Docker will download all the required dependencies. Start the container with
    
    docker-compose run -d -p 2016:9999 pymosek
    

## License

If you have a valid Mosek license you may want to edit the Dockerfile and adjust the definition of the environment variable in there.

## Applications

You can solve various (un)constrained regression and Markowitz problems.








