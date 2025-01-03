# [MosekTools](https://tschm.github.io/MosekRegression/book)

Building tools on the shoulders of [Mosek](http://www.mosek.com).

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/MosekRegression)

## Motivation

We created this package to support the experiments given in the [paper](http://arxiv.org/abs/1310.3397)
by Schmelzer, Hauser, Dahl and Andersen.

## License

You need a valid Mosek license.

## Applications

You can solve various (un)constrained regression and Markowitz problems.

## Poetry

We assume you share already the love for [Poetry](https://python-poetry.org).
Once you have installed poetry you can perform

```bash
make install
```

to replicate the virtual environment we have defined in [pyproject.toml](pyproject.toml)
and locked in [poetry.lock](poetry.lock).

## Jupyter

We install [JupyterLab](https://jupyter.org) on fly within the aforementioned
virtual environment. Executing

```bash
make jupyter
```

will install and start the jupyter lab.
